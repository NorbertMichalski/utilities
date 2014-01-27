from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
#from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'utilities.views.home', name='home'),
    # url(r'^utilities/', include('utilities.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #custom admin view
    url(r'^admin/tutorials/tutorials/$', 'tutorials.views.tutorials_view'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'utilities.views.home'),
    url(r'^supply/', include('supply.urls', namespace="supply")),
    url(r'^tracking/', include('tracking.urls', namespace="tracking")),
    url(r'^shipping/', include('shipping.urls', namespace="shipping")),
    url(r'^resale_cert/', include('resale_cert.urls', namespace="resale_cert")),
    url(r'^chat/', include('djangoChat.urls')),
    
    #url(r'^media/', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT})
    url(r'^favicon\.ico$', RedirectView.as_view(url='shopmro.com/utilities/favicon.ico')),

)
