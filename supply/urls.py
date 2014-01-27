from django.conf.urls import patterns, url

from supply import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^availability$', views.availability, name='availability'),
    url(r'^baldor/(.*)/$', views.baldor_availability, name='baldor_availability'),
    url(r'^calculate_distances/$', views.calculate_distances, name='calculate_distances'),
    url(r'^calculate_distances1/$', views.calculate_distances1, name='calculate_distances1'),
    url(r'^weight/$', views.get_weight, name='get_weight'),
)


# url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
