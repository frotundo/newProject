"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from lims import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

def login_view(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                if User.objects.get(username = username).first_name == models.Cliente.objects.get(titular=User.objects.get(username = username).first_name).titular:
                    login(request, user)
                    return redirect('users:client_index', User.objects.get(username = username).username)
            except:
                login(request, user)
                return redirect('lims:index')
        else:
            return render(request, 'users/login.html', {
                'error' : 'Nombre de usuario o contraseña inválida.',
                })

    return render(request, 'users/login.html')


def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('users:login')

@login_required
def client_index(request, username):
    usuario = User.objects.get(username = username)
    cliente = models.Cliente.objects.get(titular=usuario.first_name)
    parametros = models.ParametroDeMuestra.objects.select_related('servicio').all()
    parametros = parametros.select_related('parametro').all().order_by('-codigo_servicio')
    queryset_projects = models.Proyecto.objects.filter(cliente_id=cliente.id).order_by('-created')
    paginator_projects = Paginator(queryset_projects, 5)
    page_project = request.GET.get('page_project')
    projects = paginator_projects.get_page(page_project)
    
    return render(request, 'lims/client_index.html', {
        'cliente': cliente,
        'parametros': parametros,
        'usuario': usuario,
        'projects': projects,
    })