from django.conf.urls import url
from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^list/$', views.organizations_list, name='list'),
    url(r'^create/$', views.add_org, name='add_org'),
    ]
