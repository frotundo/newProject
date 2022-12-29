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

    if request.method == 'POST':
        titular = request.POST['titular']
        rut = request.POST['rut']
        direccion = request.POST['direccion']
        actividad = request.POST['actividad']
        usuario = request.POST['creador']
        models.Cliente.objects.create(titular=titular, rut=rut, direccion=direccion, actividad=actividad, creator_user=usuario)

        return redirect('lims:clients')
    return render(request, 'LIMS/add_client.html')


@login_required
def client(request, id_cliente):
    """Client model."""
    cliente = models.Cliente.objects.get(id=id_cliente)
    contacts = models.ContactoCliente.objects.filter(cliente_id = id_cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente)
    legal_representatives = models.RepresentanteLegalCliente.objects.filter(cliente_id = id_cliente)
    rcas = models.RCACliente.objects.filter(cliente_id = id_cliente)
    return render(request, 'LIMS/client.html', {
        'cliente':cliente,
        'contacts': contacts,
        'sample_points':sample_points,
        'legal_representatives': legal_representatives,
        'rcas': rcas,
    })


def client_add_legal_representative(request, id_cliente):
    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/client_add_legal_representative.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            contactos = todo[1::3]
            ruts = todo[2::3]
            usuarios = todo[3::3]
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.RepresentanteLegalCliente.objects.create(nombre= contacto, rut=rut, cliente_id= id_cliente, creator_user= usuario) 
            return redirect('lims:client', id_cliente)
    return render(request, 'lims/client_add_legal_representative.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_contact(request, id_cliente):
    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/client_add_contact.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            contactos = todo[1::3]
            ruts = todo[2::3]
            usuarios = todo[3::3]
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.ContactoCliente.objects.create(nombre= contacto, rut=rut, cliente_id= id_cliente, creator_user= usuario) 
            return redirect('lims:client', id_cliente)
    return render(request, 'lims/client_add_contact.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_sample_point(request, id_cliente):
    '''Client add sample point view.'''

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/client_add_sample_point.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            usuarios = todo[2::2]
            for punto, usuario in zip(puntos, usuarios):
                models.PuntoDeMuestreo.objects.create(nombre= punto, cliente_id= id_cliente, creator_user= usuario) 
            return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_sample_point.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_rca(request, id_cliente):
    '''Client add sample point view.'''

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/client_add_rca.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            usuarios = todo[2::2]
            for punto, usuario in zip(puntos, usuarios):
                models.RCACliente.objects.create(rca_asociada= punto, cliente_id= id_cliente, creator_user= usuario) 
            return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_rca.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def normas_ref(request):
    """Normas de referencias view."""

    normas = models.NormaDeReferencia.objects.all()
    return render(request, 'LIMS/normas_ref.html',{
        'normas': normas,
    })


@login_required
def add_normas_ref(request):
    """Add Standards of reference view."""

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/add_normas_ref.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            normas = todo[1::2]
            usuarios = todo[2::2]
            for norma, usuario in zip(normas, usuarios):
                models.NormaDeReferencia.objects.create(norma=norma, creator_user=usuario) 
            return redirect('lims:normas_ref')

    return render(request, 'LIMS/add_normas_ref.html', {
        'pm':[0],
        'len_pm': 1,
    })

@login_required
def methods(request):
    """Normas de referencias view."""

    metodos = models.Metodo.objects.all()
    return render(request, 'LIMS/methods.html',{
        'metodos': metodos,
    })


@login_required
def add_method(request):
    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/add_method.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            metodos = todo[1::2]
            usuarios = todo[2::2]
            for nombre, usuario in zip(metodos, usuarios):
                models.Metodo.objects.create(nombre= nombre, creator_user=usuario) 
            return redirect('lims:methods')
    return render(request, 'lims/add_method.html', {
        'pm':[0],
        'len_pm': 1,
    })

@login_required
def containers(request):
    '''Containers view.'''

    envases = models.Envase.objects.all()
    return render(request, 'LIMS/containers.html',{
        'envases': envases,
    })

@login_required
def add_container(request):
    """Add container view."""

    if request.method == 'POST':
        nombre = request.POST['nombre']
        volumen = request.POST['volumen']
        material = request.POST['material']
        preservante = request.POST['preservante']
        usuario = request.POST['creador']
        models.Envase.objects.create(nombre=nombre, volumen=volumen, material=material, preservante=preservante, creator_user=usuario)

        return redirect('lims:containers')
    return render(request, 'LIMS/add_containers.html')