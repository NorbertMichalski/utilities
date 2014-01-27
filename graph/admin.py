from django.contrib import admin
#from django.utils.translation import ugettext as _
#from django.utils.encoding import force_unicode
from django.http import HttpResponseRedirect
from graph.models import OverviewGraph, OverviewStat


class OverviewGraphAdmin(admin.ModelAdmin):
    list_display = ('brand',)
    
    readonly_fields = ('chart', )
    fieldsets = [
                 #('Details', { 'fields':  [  'brand',]}),
                 ('Chart', { 'fields':  [  'chart',  ]}),
                ]
    
    # Remove the delete Admin Action for this Model
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        #Return nothing to make sure user can't update any data
        pass
    
    
    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.has_key("_viewnext"):
            msg = ('Next Chart')
            next = obj.__class__.objects.filter(id__gt=obj.id).order_by('id')[:1]
            if next:
                self.message_user(request, msg)
                return HttpResponseRedirect("../%s/" % next[0].pk)
            else:
                self.message_user(request, msg)
                return HttpResponseRedirect("../1/")
        return super(OverviewGraphAdmin, self).response_change(request, obj)
    

class OverviewStatAdmin(admin.ModelAdmin):
    list_display = ('graph', 'price', 'rank', 'sales', 'visits', 'date')
    
    fieldsets = [
     ('Details', { 'fields':  [  'graph', 'price', 'rank',
                    'sales', 'visits', 'date']}),

                ]


admin.site.register(OverviewGraph, OverviewGraphAdmin)
#admin.site.register(OverviewStat, OverviewStatAdmin)
