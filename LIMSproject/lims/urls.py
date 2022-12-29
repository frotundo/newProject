"""LIMS urls."""

from django.urls import path

from . import views

app_name= 'lims'
urlpatterns = [
    path('', views.index, name="index"),
    path('clients/', views.clients, name="clients"),
    path('clients/<int:id_cliente>/', views.client, name="client"),
    path('add_client/', views.add_client, name="add_client"),
    path('clients/<int:id_cliente>/add_legal_representative/', views.client_add_legal_representative, name="client_add_legal_representative"),
    path('clients/<int:id_cliente>/add_contact/', views.client_add_contact, name="client_add_contact"),
    path('clients/<int:id_cliente>/add_sample_point/', views.client_add_sample_point, name="client_add_sample_point"),
    path('clients/<int:id_cliente>/add_rca/', views.client_add_rca, name="client_add_rca"),
    path('normas_ref/add_norma/', views.add_normas_ref, name="add_normas_ref"),
    path('normas_ref/', views.normas_ref, name="normas_ref"),
    path('methods/', views.methods, name="methods"),
    path('methods/add_method/', views.add_method, name="add_method"),
    path('containers/', views.containers, name="containers"),
    path('containers/add_container/', views.add_container, name="add_containers"),
]
