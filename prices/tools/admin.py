from django.contrib import admin
from models import Proxy, UploadProduct, UpdatePrice


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('address', 'port', 'username')


class UpdatePriceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'uploaded_at', 'successfully_updated', 'failed_entries')


class UploadProductAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'uploaded_at', 'successfully_updated', 'failed_entries')


admin.site.register(Proxy, ProxyAdmin)
admin.site.register(UpdatePrice, UpdatePriceAdmin)
admin.site.register(UploadProduct, UploadProductAdmin)



