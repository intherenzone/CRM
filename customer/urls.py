from django.conf.urls import url
from customer import views

app_name = 'customer'

urlpatterns = [
    url(r'^list/$', views.customer_list, name='list'),
    url(r'^create/$', views.add_customer, name='add_customer'),
    ]
