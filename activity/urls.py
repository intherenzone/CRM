from django.conf.urls import url
from activity import views

app_name = 'activity'

urlpatterns = [
    url(r'^list/$', views.activity_list, name='list'),
    url(r'^create/$', views.add_activity, name='add_activity'),
    url(r'^create/$', views.add_activity, name='save'),
    url(r'^delete/(?P<pk>\d+)$', views.remove_activity, name='remove_activity'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit_activity, name='edit_activity'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit_activity, name='save'),
    ]
