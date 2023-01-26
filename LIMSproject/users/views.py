"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from lims.models import Cliente


# Create your views here.

def login_view(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                if User.objects.get(username = username).first_name == Cliente.objects.get(titular=User.objects.get(username = username).first_name).titular:
                    print('si')
                    login(request, user)
                    return redirect('lims:client_index', User.objects.get(username = username).username)
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