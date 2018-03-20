from django.conf.urls import url
from activity import views

app_name = 'activity'

urlpatterns = [
    url(r'^list/$', views.activity_list, name='list'),
    url(r'^create/$', views.add_activity, name='add_activity'),
    url(r'^(?P<activity_id>\d+)/view/$', views.view_activity, name='view_activity'),
    url(r'^delete/(?P<pk>\d+)/remove/$', views.remove_activity, name='remove_activity'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit_activity, name='edit_activity'),

    #url(r'^get/list/$', views.get_avtivity, name='get_activity'),
    # comments
    url(r'^comment/add/$', views.add_comment, name='add_comment'),
    url(r'^comment/edit/$', views.edit_comment, name='edit_comment'),
    url(r'^comment/remove/$', views.remove_comment, name='remove_comment'),

    #calendar
    url(r'^calendar/syn/(?P<user>[\w\-]+)', views.calendar_syn, name='calendar_syn'),
    url(r'^(?P<activity_id>\d+)/calendar/export/$', views.export_calendar, name='export_calendar'),
    url(r'^calendar/url/$', views.calendar_url, name='calendar_url'),
    ]
