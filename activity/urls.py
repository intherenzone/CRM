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
    url(r'^(?P<pk>\d+)/view/$', views.view_activity, name='view_activity'),
    # comments
    url(r'^comment/add/$', views.add_comment, name='add_comment'),
    url(r'^comment/edit/$', views.edit_comment, name='edit_comment'),
    url(r'^comment/remove/$', views.remove_comment, name='remove_comment'),
    ]
