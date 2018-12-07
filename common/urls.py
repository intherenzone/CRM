from django.conf.urls import url
from common import views
from django.contrib.auth import views as auth_views

app_name = 'common'


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', views.login_crm, name="home"),
    url(r'^registration/$', views.register_page, name='create'),
    url(r'^newsfeed/$',views.newsfeed, name="newsfeed"),
    url(r'^view_profile/$',views.view_profile,name="view_profile"),
    url(r'^(?P<user_id>\d+)/edit_profile/$',views.edit_profile,name="edit_profile"),
]
