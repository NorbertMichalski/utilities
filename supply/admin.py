from django.contrib import admin
from supply.models import Location, Brand, Product
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"


# admin.site.register(Location)
admin.site.register(Brand)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('brand', 'city_state', 'slug', 'address', 'zip', 'latitude', 'longitude', 'timezone', 'timediff', 'phone')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('mro_id', 'part_number', 'brand', 'weight', 'updated')
    list_filter = ('brand__name', 'updated')
    search_fields = ['mro_id', 'part_number', 'brand__name', 'weight']
    actions = [download_csv]

admin.site.register(Location, LocationAdmin)
admin.site.register(Product, ProductAdmin)
