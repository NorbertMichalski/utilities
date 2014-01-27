from django.conf.urls import patterns, url

from tracking import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

)
