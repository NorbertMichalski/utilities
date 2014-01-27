from django.conf.urls import patterns, url

from shipping import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^estimate/$', views.estimate, name='estimate'),
    url(r'^international/$', views.international, name='international'),
)
