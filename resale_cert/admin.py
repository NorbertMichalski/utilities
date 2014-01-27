from django.contrib import admin
from resale_cert.models import Reseller

# admin.site.register(Reseller)

class ResellerAdmin(admin.ModelAdmin):
    list_display = ('permit_number', 'validation', 'owner', 'bussiness_name', 'address', 'city', 'state', 'start_date')

admin.site.register(Reseller, ResellerAdmin)

