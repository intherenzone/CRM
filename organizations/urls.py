from django.conf.urls import url
from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^list/$', views.organizations_list, name='list'),
    url(r'^create/$', views.add_organization, name='add_organization'),
    url(r'^(?P<organization_id>\d+)/view/$', views.view_organization, name='view_organization'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit_organization, name='edit_organization'),
    url(r'^(?P<pk>\d+)/remove/$', views.remove_organization, name='remove_organization'),
    url(r'^get/list/$', views.get_organizations, name='get_organizations'),
    # comments
    url(r'^comment/add/$', views.add_comment, name='add_comment'),
    url(r'^comment/edit/$', views.edit_comment, name='edit_comment'),
    url(r'^comment/remove/$', views.remove_comment, name='remove_comment'),
]
