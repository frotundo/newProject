"""LIMS urls."""

from django.urls import path

from . import views

app_name= 'lims'
urlpatterns = [
    path('', views.index, name="index"),
    path('client', views.client, name="client"),
    path('add_client', views.add_client, name="add_client"),
    path('add_sample_point', views.add_sample_point, name="add_sample_point"),
]
