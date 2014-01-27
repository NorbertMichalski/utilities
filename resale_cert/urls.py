from django.conf.urls import patterns, url

from resale_cert import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

)
