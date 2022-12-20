from django.urls import path

from . import views

app_name= 'lims'
urlpatterns = [
    path('', views.index, name="index"),
]
