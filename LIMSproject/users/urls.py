"""Users urls."""

from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/', views.client_index, name="client_index"),
]
