from django.contrib import admin
from django.contrib.sites.models import Site
from models import Competitor, Brand, Product, Result, Archive, LeesonReport, BaldorReport, RedlionReport, DodgeReport
from django.utils.translation import ugettext_lazy as _
import csv
import inspect
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    # opts = modeladmin.model._meta
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


def report_download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    # opts = modeladmin.model._meta
    opts = queryset.model._meta
    model = queryset.model
    # find out on which report we are
    brand_name = model.__name__.split('Report')[0]
    brand = Brand.objects.filter(name=brand_name)
    brand_competitors = Competitor.objects.filter(brand__in=brand)
    name_competitors = [str(competitor.name) for competitor in brand_competitors]

    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # field_names.extend(func_competitors)
    # Write a first row with header information
    writer.writerow(field_names + name_competitors)
    # Write data rows
    for obj in queryset:
        # the fields
        data = [getattr(obj, field) for field in field_names]
        # the results of the methods
        data1 = [getattr(obj, func)() for func in name_competitors]
        data.extend(data1)
        writer.writerow(data)
    return response
report_download_csv.short_description = "Download selected as csv"


def result_download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    # opts = modeladmin.model._meta
    opts = queryset.model._meta
    model = queryset.model
    # find out on which report we are

    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    func_names = [field.name for field in opts.fields]
    # field_names.extend(func_competitors)
    # Write a first row with header information
    data = ['Competitor', 'MRO id', 'Part Number', 'MRO Price', 'New Price',
                    'Date Scraped', 'Old Price', 'Previous Date', 'Percentage Change' ]
    writer.writerow(data)
    # Write data rows
    for result in queryset:
        product_id = result.product
        competitor_id = result.competitor
        mro_id = result.product.mro_id
        part_number = result.product.part_number
        competitor = result.competitor.name
        brand = result.product.brand.name
        price = result.price
        old_price = result.previous_price()
        mro_price = result.MRO_price()
        previous_date = result.previous_date()
        date = result.scraped
        percentage_changed = result.percentage_change()
        data = [competitor, mro_id, part_number,mro_price, price, date, old_price, previous_date, percentage_changed ]
        writer.writerow(data)
    return response
result_download_csv.short_description = "Download selected as csv"


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'last_scrap')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('mro_id', 'part_number', 'brand', 'mro_price', 'updated', 'is_cheaper')
    list_filter = ('brand__name', 'updated', 'is_cheaper')
    search_fields = ['mro_id', 'part_number', 'brand__name']
    actions = [download_csv]

class ResultAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'brand', 'MRO_id', 'product', 'MRO_price', 'price', 'scraped', 'previous_price', 'previous_date', 'percentage_change', 'is_cheaper', 'changed', )
    list_filter = ('competitor__name', 'product__brand__name', 'scraped', 'is_cheaper', 'changed')
    search_fields = ['competitor__name', 'product__part_number', 'product__brand__name', 'product__mro_id']
    actions = [result_download_csv]

class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'product', 'price', 'scraped')
    list_filter = ('competitor__name', 'product__brand__name', 'scraped')
    search_fields = ['competitor__name', 'product__part_number', 'product__brand__name', 'product__mro_id']
    actions = [download_csv]

class BaldorReportAdmin(admin.ModelAdmin):
    brand = Brand.objects.filter(name='Baldor')
    brand_competitors = Competitor.objects.filter(brand__in=brand)
    competitors = [str(competitor.name) for competitor in brand_competitors]
    list_display1 = ['mro_id', 'part_number', 'brand', 'mro_price']
    list_display1.extend(competitors)
    list_display = list_display1
    list_filter = ('updated', 'is_cheaper')
    search_fields = ['mro_id', 'part_number']
    actions = [report_download_csv]

    def queryset(self, request):
        return self.model.objects.filter(brand__name="Baldor")


class RedlionReportAdmin(admin.ModelAdmin):
    brand = Brand.objects.filter(name='Redlion')
    brand_competitors = Competitor.objects.filter(brand__in=brand)
    competitors = [str(competitor.name) for competitor in brand_competitors]
    list_display1 = ['mro_id', 'part_number', 'brand', 'mro_price']
    list_display1.extend(competitors)
    list_display = list_display1
    list_filter = ('updated', 'is_cheaper')
    search_fields = ['mro_id', 'part_number']
    actions = [report_download_csv]

    def queryset(self, request):
        return self.model.objects.filter(brand__name="Redlion")


class LeesonReportAdmin(admin.ModelAdmin):
    brand = Brand.objects.filter(name='Leeson')
    brand_competitors = Competitor.objects.filter(brand__in=brand)
    competitors = [str(competitor.name) for competitor in brand_competitors]
    list_display1 = ['mro_id', 'part_number', 'brand', 'mro_price']
    list_display1.extend(competitors)
    list_display = list_display1
    list_filter = ('updated', 'is_cheaper')
    search_fields = ['mro_id', 'part_number']
    actions = [report_download_csv]

    def queryset(self, request):
        return self.model.objects.filter(brand__name="Leeson")


class DodgeReportAdmin(admin.ModelAdmin):
    brand = Brand.objects.filter(name='Dodge')
    brand_competitors = Competitor.objects.filter(brand__in=brand)
    competitors = [str(competitor.name) for competitor in brand_competitors]
    list_display1 = ['mro_id', 'part_number', 'brand', 'mro_price']
    list_display1.extend(competitors)
    list_display = list_display1
    list_filter = ('updated', 'is_cheaper')
    search_fields = ['mro_id', 'part_number']
    actions = [report_download_csv]

    def queryset(self, request):
        return self.model.objects.filter(brand__name="Dodge")

admin.site.unregister(Site)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Result, ResultAdmin)
# admin.site.register(Archive, ArchiveAdmin)
admin.site.register(BaldorReport, BaldorReportAdmin)
admin.site.register(RedlionReport, RedlionReportAdmin)
admin.site.register(LeesonReport, LeesonReportAdmin)
admin.site.register(DodgeReport, DodgeReportAdmin)

