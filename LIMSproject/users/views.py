"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.

def login_view(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
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