"""LIMS views."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import models

# Create your views here.

@login_required
def index(request):
    """Index view."""
   
    return render(request, 'base/base.html')

@login_required
def clients(request):
    """Clients view."""
    
    clients = models.Cliente.objects.all()
    return render(request, 'LIMS/clients.html', {
        'clients': clients,
    })


@login_required
def add_client(request):
    """Add client view."""
    # ID = len(models.Cliente.objects.all())
    if request.method == 'POST':
        titular = request.POST['titular']
        rut = request.POST['rut']
        direccion = request.POST['direccion']
        actividad = request.POST['actividad']
        models.Cliente.objects.create(titular=titular, rut=rut, direccion=direccion, actividad=actividad)

        return redirect('lims:clients')
    return render(request, 'LIMS/add_client.html')


@login_required
def client(request, id_cliente):
    """Client model."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    return render(request, 'LIMS/client.html', {
        'cliente':cliente,
    })
    


@login_required
def sample_points(request):
    """Sample point view."""
    clients = models.Cliente.objects.all()
    sp = models.PuntoDeMuestreo.objects.all()
    return render(request, 'LIMS/sample_points.html', {
        'sp': sp,
        'clients': clients,
    })


@login_required
def client_sample_points(request, id_client):
    '''Client sample points views'''
    pass

@login_required
def add_sample_point(request):
    """Add sample point view."""

    clientes = models.Cliente.objects.all()
    sp = models.PuntoDeMuestreo.objects.all()
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
            return render(request, 'lims/sample_point.html', {
                'sp': sp,
                'clients': clientes,
                # 'error': error,
                })
    return render(request, 'lims/add_sample_point.html', {
        'pm':[0],
        'len_pm': 1,
        'clientes': clientes,
    })


@login_required
def contact(request):
    """Contact view."""
    clients = models.Cliente.objects.all()
    contacts = models.ContactoCliente.objects.all()
    return render(request, 'LIMS/contact.html', {
        'contacts': contacts,
        'clients': clients,
    })


@login_required
def add_contact(request):
    """Add sample point view."""

    clientes = models.Cliente.objects.all()
    sp = models.PuntoDeMuestreo.objects.all()
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
            return render(request, 'lims/sample_point.html', {
                'sp': sp,
                'clients': clientes,
                # 'error': error,
                })
    return render(request, 'lims/add_contact.html', {
        'pm':[0],
        'len_pm': 1,
        'clientes': clientes,
    })