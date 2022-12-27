"""LIMS views."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import models

# Create your views here.

@login_required
def index(request):
    """Index view."""
    clientes = models.Cliente.objects.all()
    print(clientes)
    if request.method == 'POST':
        print('cliente' not in request.POST.keys())
        client = request.POST['cliente']
        puntos = []
        for valor in request.POST.values():
           puntos.append(valor)
        puntos = puntos[2::]
        print(client)
        # for punto in puntos:
        #     if punto == "":
        #         continue
        #     else:
        #         models.PuntoDeMuestreo.objects.create(nombre= punto, cliente_id= client) 
    return render(request, 'lims/pruebas.html', {
        'pm':[0,1,2],
        'clientes': clientes,
    })

@login_required
def client(request):
    """Client view."""
    
    clients = models.Cliente.objects.all()
    # if clients == 0:
    #     error = 'No hay clientes disponibles.'
    return render(request, 'LIMS/client.html', {
        'clients': clients,
        # 'error': error,
    })

@login_required
def add_client(request):
    """Add client view."""
    ID = len(models.Cliente.objects.all())
    if request.method == 'POST':
        titular = request.POST['titular']
        rut = request.POST['rut']
        direccion = request.POST['direccion']
        actividad = request.POST['actividad']
        models.Cliente.objects.create(titular=titular, rut=rut, direccion=direccion, actividad=actividad)

        return redirect('lims:client')
    return render(request, 'lims/add_client.html')

@login_required
def add_sample_point(request):
    """Add sample point view."""
    clientes = models.Cliente.objects.all()
    
    if request.method == 'POST':
        if 'cliente' not in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/add_sample_point.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    'clientes': clientes,
                    })
        else:
            client = request.POST['cliente']
            puntos = []
            for valor in request.POST.values():
                puntos.append(valor)
            puntos = puntos[2::]
            print(puntos)
            for punto in puntos:
                if punto == "":
                    continue
                else:
                    models.PuntoDeMuestreo.objects.create(nombre= punto, cliente_id= client) 
    return render(request, 'lims/add_sample_point.html', {
        'pm':[0],
        'clientes': clientes,
    })