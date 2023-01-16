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
    path('clients/<int:id_cliente>/add_project/', views.client_add_project, name="client_add_project"),
    path('normas_ref/add_norma/', views.add_normas_ref, name="add_normas_ref"),
    path('normas_ref/', views.normas_ref, name="normas_ref"),
    path('methods/', views.methods, name="methods"),
    path('methods/add_method/', views.add_method, name="add_method"),
    path('containers/', views.containers, name="containers"),
    path('containers/add_container/', views.add_container, name="add_containers"),
    path('parameters/', views.parameters, name="parameters"),
    path('parameters/add_parameter/', views.add_parameter, name="add_parameter"),
    path('samples_type/', views.samples_type, name="samples_type"),
    path('samples_type/add_sample_type/', views.add_sample_type, name="add_sample_type"),
    path('etfa/', views.etfa, name="etfa"),
    path('etfa/add_etfa', views.add_etfa, name="add_etfa"),
    path('project/<str:project_id>/', views.project, name="project"),
    path('project/<str:project_id>/add_service', views.add_service, name="add_service"),
    path('service/<str:service_id>/', views.service, name="service"),
    path('service/<str:service_id>/add_service_parameter', views.add_service_parameter, name="add_service_parameter"),
    path('parameter/<str:parameter_id>/', views.edit_sample_parameter, name="edit_sample_parameter"),
    path('service_parameters/', views.service_parameters, name="service_parameters"),
    path('service_parameters_filter/', views.service_parameters_filter, name="service_parameters_filter"),
    path('projects/', views.projects, name="projects"),
    path('services/', views.services, name="services"),
    ]
