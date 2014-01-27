from django.contrib import admin
from tracking.models import Shipping


class ShippingAdmin(admin.ModelAdmin):
    fields = ['orderNumber', 'company', 'trackNumber', 'dateAdded' ]
    list_display = ('orderNumber', 'company', 'trackNumber', 'dateAdded')
    list_filter = ['dateAdded']
    search_fields = ['orderNumber']

#admin.site.register(Shipping, ShippingAdmin)


