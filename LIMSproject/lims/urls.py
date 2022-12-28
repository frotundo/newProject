"""LIMS urls."""

from django.urls import path

from . import views

app_name= 'lims'
urlpatterns = [
    path('', views.index, name="index"),
    path('clients', views.clients, name="clients"),
    path('client', views.client, name="client"),
    path('add_client', views.add_client, name="add_client"),
    path('client/<int:id_client>/sample_points', views.client_sample_points, name="client_sample_points"),
    path('contact', views.contact, name="contact"),
    path('add_contact', views.add_contact, name="add_contact"),
    path('add_sample_point', views.add_sample_point, name="add_sample_point"),
    path('sample_points', views.sample_points, name="sample_points"),
]
