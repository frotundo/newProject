"""LIMS views."""

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

from datetime import datetime

from . import models, forms
from datetime import datetime
from workdays import workday


import pandas as pd
# Create your views here.



def add_workdays(start_date, num_workdays):
    end_date = workday(start_date, num_workdays)
    return end_date

def list_to_string(lista):
    if len(lista)==2:
        return ' y '.join(lista)
    else:
        return ', '.join(lista)


@login_required
def index(request):
    """Index view."""
    return render(request, 'lims/menu.html')


@login_required
def clients(request):
    """Clients view."""

    clientes = models.Cliente.objects.all().order_by('titular')
    paginator = Paginator(clientes, 25)
    page = request.GET.get('page')
    clients = paginator.get_page(page)

    if request.method == 'POST':
        if request.POST['search_text'] == '' or request.POST['opcion'] == '':
            return render(request, 'LIMS/clients.html', {
                'clients': clients,
            })
        elif request.POST['opcion'] == 'titular':
            clientes = models.Cliente.objects.filter(titular__icontains = request.POST['search_text']).order_by('titular')
            paginator = Paginator(clientes, 25)
            page = request.GET.get('page')
            clients = paginator.get_page(page)
            return render(request, 'LIMS/clients.html',{
                'clients': clients,
                })


        elif request.POST['opcion'] == 'rut':
            clientes = models.Cliente.objects.filter(rut__contains = request.POST['search_text']).order_by('titular')
            paginator = Paginator(clientes, 25)
            page = request.GET.get('page')
            clients = paginator.get_page(page)
            return render(request, 'LIMS/clients.html',{
                'clients': clients,
                })
    
    
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
        try:
            models.Cliente.objects.create(
                titular=titular, 
                rut=rut, 
                direccion=direccion, 
                actividad=actividad, 
                creator_user=usuario
                )
            return redirect('lims:clients')
        except:
            error = "El titular o el RUT ya existe."
            return render(request, 'LIMS/add_client.html', {
                'error_client': error,
            })

    return render(request, 'LIMS/add_client.html')


@login_required
def client(request, id_cliente):
    """Client model."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    
    queryset_contacts = models.ContactoCliente.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_contact = Paginator(queryset_contacts, 5)
    page_contact = request.GET.get('page_contact')
    contacts = paginator_contact.get_page(page_contact)

    queryset_sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_sp = Paginator(queryset_sample_points, 5)
    page_sp = request.GET.get('page_sp')
    sample_points = paginator_sp.get_page(page_sp)
    
    queryset_legal_representatives = models.RepresentanteLegalCliente.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_lr = Paginator(queryset_legal_representatives, 5)
    page_lr = request.GET.get('page_lr')
    legal_representatives = paginator_lr.get_page(page_lr)

    queryset_rcas = models.RCACliente.objects.filter(cliente_id = id_cliente).order_by('rca_asociada')
    paginator_rca = Paginator(queryset_rcas, 5)
    page_rca = request.GET.get('page_rca')
    rcas = paginator_rca.get_page(page_rca)

    queryset_projects = models.Proyecto.objects.filter(cliente_id = id_cliente).order_by('codigo')
    paginator_projects = Paginator(queryset_projects, 5)
    page_project = request.GET.get('page_project')
    projects = paginator_projects.get_page(page_project)

    return render(request, 'LIMS/client.html', {
        'cliente':cliente,
        'contacts': contacts,
        'sample_points':sample_points,
        'legal_representatives': legal_representatives,
        'rcas': rcas,
        'projects': projects,
    })


@login_required
def client_add_legal_representative(request, id_cliente):
    """Client add legal representative view."""

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
            duplicados = []
            for rut in ruts:
                try:
                    if rut == models.RepresentanteLegalCliente.objects.get(rut=rut).rut:
                            duplicados.append(rut) 
                            duplicado =  ruts.index(rut)
                            usuarios.pop(duplicado)
                            contactos.pop(duplicado)
                            ruts.pop(duplicado)
                except:
                    continue
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.RepresentanteLegalCliente.objects.create(
                    nombre= contacto.title(), 
                    rut=rut, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                return render(request, 'lims/client_add_legal_representative.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:client', id_cliente)
    
    return render(request, 'lims/client_add_legal_representative.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_contact(request, id_cliente):
    """Client add contact view."""

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
            duplicados = []
            for rut in ruts:
                try:
                    if rut == models.ContactoCliente.objects.get(rut=rut).rut:
                            duplicados.append(rut) 
                            duplicado =  ruts.index(rut)
                            usuarios.pop(duplicado)
                            contactos.pop(duplicado)
                            ruts.pop(duplicado)
                except:
                    continue
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.ContactoCliente.objects.create(
                    nombre= contacto.title(), 
                    rut=rut, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                return render(request, 'lims/client_add_contact.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
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
            duplicados = []
            for punto in puntos:
                try:
                    if punto == models.PuntoDeMuestreo.objects.get(nombre=punto).nombre:
                            duplicados.append(punto) 
                            duplicado =  puntos.index(punto)
                            usuarios.pop(duplicado)
                            puntos.pop(duplicado)
                except:
                    continue
            for punto, usuario in zip(puntos, usuarios):
                models.PuntoDeMuestreo.objects.create(
                    nombre= punto, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El punto de muestreo {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los puntos de muestreo: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                return render(request, 'LIMS/client_add_sample_point.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:        
                return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_sample_point.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_rca(request, id_cliente):
    '''Client add RCA view.'''

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
            duplicados = []
            for rca in puntos:
                try:
                    if rca == models.RCACliente.objects.get(rca_asociada=rca).rca_asociada:
                            duplicados.append(rca) 
                            duplicado =  puntos.index(rca)
                            usuarios.pop(duplicado)
                            puntos.pop(duplicado)
                except:
                    continue
            for punto, usuario in zip(puntos, usuarios):
                models.RCACliente.objects.create(
                    rca_asociada= punto, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RCA {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RCA: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                return render(request, 'LIMS/add_normas_ref.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_rca.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def client_add_project(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente)
    rcas = models.RCACliente.objects.filter(cliente_id = id_cliente)
    normas = models.NormaDeReferencia.objects.all()
    matrices = models.TipoDeMuestra.objects.all()
    
    if request.method == 'POST':
        client = request.POST['cliente']
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        creator_user = request.POST['creator_user']
        try:
            models.Proyecto.objects.create(
            codigo=codigo, 
            nombre=nombre, 
            creator_user=creator_user,
            cliente_id=client)

            return redirect('lims:client', id_cliente)
        except:
            error = "El Codigo de Proyecto ya existe."
            return render(request, 'LIMS/client_add_project.html', {
                'sample_points' : sample_points,
                'rcas': rcas,
                'normas': normas,
                'matrices': matrices,
                'cliente': cliente,
                'error_client': error,
            })
    
    return render(request, 'LIMS/client_add_project.html', {
        'sample_points' : sample_points,
        'rcas': rcas,
        'normas': normas,
        'matrices': matrices,
        'cliente': cliente,
    })


def client_add_project_cot(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    parameters = models.ParametroEspecifico.objects.filter(codigo_etfa = None).order_by('ensayo')
    
    if request.method == 'POST':
        client = request.POST['cliente']
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        creator_user = request.POST['creator_user']
        parametros = request.POST.getlist('parameters')
        
        try:
            project = models.Proyecto.objects.create(
                codigo=codigo, 
                nombre=nombre, 
                creator_user=creator_user,
                cliente_id=client, 
                cotizado=True,
                )
            
            project.parametros_cotizados.set(parametros)

            return redirect('lims:client', id_cliente)
        except:
            error = "El Codigo de Proyecto ya existe."
            return render(request, 'LIMS/client_add_project_cot.html', {
                'cliente': cliente,
                'parameters': parameters,
                'error_client': error,
            })
    return render(request, 'LIMS/client_add_project_cot.html', {
        'cliente': cliente,
        'parameters': parameters,
    })


def client_add_project_cot_etfa(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    parameters = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo')
    
    if request.method == 'POST':
        print(request.POST)
        client = request.POST['cliente']
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        creator_user = request.POST['creator_user']
        parametros = request.POST.getlist('parameters')
        try:
            project = models.Proyecto.objects.create(
                codigo=codigo, 
                nombre=nombre, 
                creator_user=creator_user,
                cliente_id=client, 
                cotizado=True,
                etfa=True
                )
            
            project.parametros_cotizados.set(parametros)

            return redirect('lims:client', id_cliente)
        except:
            error = "El Codigo de Proyecto ya existe."
            return render(request, 'LIMS/client_add_project_cot_etfa.html', {
                'cliente': cliente,
                'parameters': parameters,
                'error_client': error,
            })
    return render(request, 'LIMS/client_add_project_cot_etfa.html', {
        'cliente': cliente,
        'parameters': parameters,
    })


@login_required
def normas_ref(request):
    """Normas de referencias view."""

    queryset_normas = models.NormaDeReferencia.objects.all().order_by('norma')
    paginator = Paginator(queryset_normas, 25)
    page = request.GET.get('page')
    normas = paginator.get_page(page)

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
            duplicados = []
            for norma in normas:
                try:
                    if norma == models.NormaDeReferencia.objects.get(norma=norma).norma:
                            duplicados.append(norma) 
                            duplicado =  normas.index(norma)
                            usuarios.pop(duplicado)
                            normas.pop(duplicado)
                except:
                    continue
            for norma, usuario in zip(normas, usuarios):
                models.NormaDeReferencia.objects.create(
                    norma=norma, 
                    creator_user=usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'La norma {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Las normas: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                return render(request, 'LIMS/add_normas_ref.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:normas_ref')

    return render(request, 'LIMS/add_normas_ref.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def methods(request):
    """Normas de referencias view."""

    queryset_metodos = models.Metodo.objects.all().order_by('nombre')
    paginator = Paginator(queryset_metodos, 25)
    page = request.GET.get('page')
    metodos = paginator.get_page(page)

    return render(request, 'LIMS/methods.html',{
        'metodos': metodos,
    })


@login_required
def add_method(request):
    """Add method view."""

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
            metodos = todo[1::3]
            descripciones = todo[2::3]
            usuarios = todo[3::3]
            duplicados = []
            for metodo in metodos:
                try:
                    if metodo == models.Metodo.objects.get(nombre=metodo).nombre:
                            duplicados.append(metodo) 
                            duplicado =  metodos.index(metodo)
                            usuarios.pop(duplicado)
                            descripciones.pop(duplicado)
                            metodos.pop(duplicado)
                except:
                    continue
            for nombre, descripcion, usuario in zip(metodos, descripciones, usuarios):
                models.Metodo.objects.create(
                    nombre= nombre, 
                    descripcion= descripcion,
                    creator_user=usuario
                    ) 
            
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El método {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los métodos: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                return render(request, 'lims/add_method.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:methods')

    
    return render(request, 'lims/add_method.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def containers(request):
    '''Containers view.'''

    queryset_envases = models.Envase.objects.all().order_by('nombre')
    paginator = Paginator(queryset_envases, 25)
    page = request.GET.get('page')
    envases = paginator.get_page(page)
    
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
        models.Envase.objects.create(
            nombre=nombre, 
            volumen=volumen, 
            material=material, 
            preservante=preservante, 
            creator_user=usuario
            )

        return redirect('lims:containers')

    return render(request, 'LIMS/add_containers.html')


@login_required
def parameters(request):
    '''Parameters view.'''

    metodos = models.Metodo.objects.all()
    queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')
    paginator = Paginator(queryset_parameters, 35)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    if request.method == 'POST':
        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')
                paginator = Paginator(queryset_parameters, 25)
                page = request.GET.get('page')
                parameters = paginator.get_page(page)
                return render(request, 'lims/parameters.html',{
                    'parameters': parameters,
                    'metodos': metodos,
                })

            if request.POST['buscar'] == 'ensayo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(ensayo__icontains=request.POST['search_text']).order_by('ensayo')
                paginator = Paginator(queryset_parameters, 25)
                page = request.GET.get('page')
                parameters = paginator.get_page(page)
                return render(request, 'lims/parameters.html',{
                    'parameters': parameters,
                    'metodos': metodos,
                    })

            if request.POST['buscar'] == 'codigo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(codigo__icontains=request.POST['search_text']).order_by('ensayo')
                paginator = Paginator(queryset_parameters, 25)
                page = request.GET.get('page')
                parameters = paginator.get_page(page)
                return render(request, 'lims/parameters.html',{
                    'parameters': parameters,
                    'metodos': metodos,
                    })

            if request.POST['buscar'] == 'metodo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(metodo__icontains=request.POST['search_text']).order_by('ensayo')
                paginator = Paginator(queryset_parameters, 25)
                page = request.GET.get('page')
                parameters = paginator.get_page(page)
                return render(request, 'lims/parameters.html',{
                    'parameters': parameters,
                    'metodos': metodos,
                    })
    
    return render(request, 'lims/parameters.html', {
        'parameters': parameters,
        'metodos': metodos,
    })


@login_required
def add_parameter(request):
    """Add parameter view."""

    metodos = models.Metodo.objects.all()
    tipos_de_muestras = models.TipoDeMuestra.objects.all()
    if request.method == 'POST':
        ensayo = request.POST['ensayo']
        codigo = request.POST['codigo']
        metodo = request.POST['metodo']
        ldm = request.POST['LDM']
        lcm = request.POST['LCM']
        unidad = request.POST['unidad']
        tipo_de_muestra = request.POST['tipo_de_muestra']
        creator_user = request.POST['creator_user']

        try:
            models.ParametroEspecifico.objects.create(ensayo=ensayo, codigo= codigo, metodo= metodo, LDM= ldm, LCM= lcm, unidad=unidad, tipo_de_muestra= tipo_de_muestra, creator_user= creator_user)
            return redirect('lims:parameters')
        except:
            error = 'EL código del parametro ya existe.'
            return render(request, 'lims/add_parameter.html',{
                'metodos': metodos,
                'tipos_de_muestras': tipos_de_muestras,
                'error_parameter': error,
            })

    return render(request, 'lims/add_parameter.html',{
        'metodos': metodos,
        'tipos_de_muestras': tipos_de_muestras,
    })
    


@login_required
def samples_type(request):
    """Samples type view."""

    queryset_samples_type = models.TipoDeMuestra.objects.all().order_by('nombre')
    paginator = Paginator(queryset_samples_type, 20)
    page = request.GET.get('page')
    samples_type = paginator.get_page(page)
    
    return render(request, 'lims/samples_type.html', {
        'samples_type':samples_type,
    })


@login_required
def add_sample_type(request):
    """Add Standards of reference view."""

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'lims/add_sample_type.html', {
                    'pm':pm,
                    'len_pm': len_pm,
                    })
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            nombres = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for nombre in nombres:
                try:
                    if nombre == models.TipoDeMuestra.objects.get(nombre=nombre).nombre:
                            duplicados.append(nombre) 
                            duplicado =  nombres.index(nombre)
                            usuarios.pop(duplicado)
                            nombres.pop(duplicado)
                except:
                    continue
            for nombre, usuario in zip(nombres, usuarios):
                models.TipoDeMuestra.objects.create(
                    nombre=nombre, 
                    creator_user=usuario
                    ) 
            
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El tipo de muestra {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los tipos de muestra: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                return render(request, 'LIMS/add_sample_type.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:samples_type')

    return render(request, 'LIMS/add_sample_type.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
def etfa(request):
    """ETFA view."""

    queryset_services = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('codigo_etfa')
    paginator = Paginator(queryset_services, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    return render(request, 'lims/etfa.html',{
        'services':services,
    })


@login_required
def add_etfa(request):
    """Add ETFA view."""

    parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')
    
    if request.method == 'POST':
        form = forms.ETFAForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('lims:etfa')

    return  render(request, 'lims/add_etfa.html', {
        'parameters': parameters,
    })



@login_required
def project(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id)
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id)
    queryset_services = models.Servicio.objects.filter(proyecto_id=project_id).order_by('-created', 'codigo')
    paginator = Paginator(queryset_services, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    parameters_service = models.ParametroDeMuestra.objects.all()
    
    return render(request, 'lims/project.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'services': services,
        'parameters': parameters_service,
    })


@login_required
def project_cot(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id)
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id)
    queryset_services = models.Servicio.objects.filter(proyecto_id=project_id).order_by('-created', 'codigo')
    paginator = Paginator(queryset_services, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    parameters_service = models.ParametroDeMuestra.objects.all()
    parametros_cotizados = project.parametros_cotizados.all()
    
    return render(request, 'lims/project_cot.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'services': services,
        'parameters': parameters_service,
        'parametros_cotizados':parametros_cotizados,
    })


@login_required
def add_service(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    parametros = models.ParametroEspecifico.objects.filter(codigo_etfa = None).order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        cliente = request.POST['cliente']
        punto_de_muestreo = request.POST['punto_de_muestreo']
        tipo_de_muestra = request.POST['tipo_de_muestra']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        fecha_de_contenedores = request.POST['fecha_de_contenedores']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        etfa = False
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        
        fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]
        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if last_service.codigo_muestra[-2:] != current_year: 
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        for sp in sample_points:
            if int(punto_de_muestreo) == int(sp.id):   
                models.Servicio.objects.create(
                    codigo = codigo_de_servicio,
                    codigo_muestra = codigo_generado, 
                    proyecto_id = proyecto, 
                    punto_de_muestreo = sp.nombre,
                    tipo_de_muestra = tipo_de_muestra,
                    fecha_de_muestreo = fecha_de_muestreo,
                    observacion = observacion,
                    fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                    fecha_de_contenedores = fecha_de_contenedores,
                    norma_de_referencia = norma_de_referencia,
                    rCA = rCA,
                    etfa = etfa,
                    muestreado_por_algoritmo = muestreado_por_algoritmo,
                    creator_user = creator_user,
                    cliente = cliente,
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'lims/add_service.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
    })


@login_required
def add_service_etfa(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    parametros = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        cliente = request.POST['cliente']
        punto_de_muestreo = request.POST['punto_de_muestreo']
        tipo_de_muestra = request.POST['tipo_de_muestra']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        fecha_de_contenedores = request.POST['fecha_de_contenedores']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        etfa = True
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        
        fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]

        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if last_service.codigo_muestra[-2:] != current_year: 
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        for sp in sample_points:
            if int(punto_de_muestreo) == int(sp.id):   
                models.Servicio.objects.create(
                    codigo = codigo_de_servicio,
                    codigo_muestra = codigo_generado, 
                    proyecto_id = proyecto, 
                    punto_de_muestreo = sp.nombre,
                    tipo_de_muestra = tipo_de_muestra,
                    fecha_de_muestreo = fecha_de_muestreo,
                    observacion = observacion,
                    fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                    fecha_de_contenedores = fecha_de_contenedores,
                    norma_de_referencia = norma_de_referencia,
                    rCA = rCA,
                    etfa = etfa,
                    muestreado_por_algoritmo = muestreado_por_algoritmo,
                    creator_user = creator_user,
                    cliente = cliente,
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'lims/add_service_etfa.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
    })

@login_required
def add_service_cot(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    parametros_cot = project.parametros_cotizados.all()
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    # parametros = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        cliente = request.POST['cliente']
        punto_de_muestreo = request.POST['punto_de_muestreo']
        tipo_de_muestra = request.POST['tipo_de_muestra']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        fecha_de_recepcion = request.POST['fecha_de_recepcion']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        etfa = request.POST['etfa']
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        
        fecha_de_recepcion= datetime.strptime(fecha_de_recepcion, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_recepcion, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]

        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if 'SI' in etfa: 
            etfa=True
        else: 
            etfa=False

        if models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif last_service.codigo_muestra[-2:] != current_year: 
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        

        for sp in sample_points:
            if int(punto_de_muestreo) == int(sp.id):   
                models.Servicio.objects.create(
                    codigo = codigo_de_servicio,
                    codigo_muestra = codigo_generado, 
                    proyecto_id = proyecto, 
                    punto_de_muestreo = sp.nombre,
                    tipo_de_muestra = tipo_de_muestra,
                    fecha_de_muestreo = fecha_de_muestreo,
                    fecha_de_recepcion = fecha_de_recepcion,
                    observacion = observacion,
                    fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                    norma_de_referencia = norma_de_referencia,
                    rCA = rCA,
                    etfa = etfa,
                    muestreado_por_algoritmo = muestreado_por_algoritmo,
                    creator_user = creator_user,
                    cliente = cliente,
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'lims/add_service_cot.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'normas': normas,
        'parametros_cot': parametros_cot,
    })


@login_required
def add_service_parameter(request, service_id):
    """Add service parameter view."""

    servicio = models.Servicio.objects.get(pk=service_id)
    project = models.Proyecto.objects.get(pk = servicio.proyecto_id)
    parametros = models.ParametroEspecifico.objects.filter(codigo_etfa = None).order_by('ensayo')
    parametros_muestra = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    for pm in parametros_muestra:
        parametros = parametros.exclude(pk= pm.parametro_id)

    if request.method == 'POST':
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = service_id, 
                parametro_id= pid, 
                ensayo= ensayo.codigo,
                codigo_servicio= servicio.codigo_muestra,
                creator_user=creator_user
                ).save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'lims/add_service_parameter.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
def add_service_parameter_etfa(request, service_id):
    """Add service parameter view."""

    servicio = models.Servicio.objects.get(pk=service_id)
    project = models.Proyecto.objects.get(pk = servicio.proyecto_id)
    parametros = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo')
    parametros_muestra = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    for pm in parametros_muestra:
        parametros = parametros.exclude(pk= pm.parametro_id)
        
    if request.method == 'POST':
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = service_id, 
                parametro_id= pid, 
                ensayo= ensayo.codigo,
                codigo_servicio= servicio.codigo_muestra,
                creator_user=creator_user
                ).save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'lims/add_service_parameter_etfa.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
def service(request, service_id):
    """Service view."""

    service = models.Servicio.objects.get(pk=service_id)
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    queryset_parameters = models.ParametroDeMuestra.objects.filter(servicio_id=service_id).order_by('-created')
    paginator = Paginator(queryset_parameters, 10)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    rca = models.RCACliente.objects.get(pk=service.rCA)
    norma = models.NormaDeReferencia.objects.get(pk=service.norma_de_referencia)
    project = models.Proyecto.objects.get(pk=service.proyecto_id)
    print(project.codigo)
    return render(request, 'lims/service.html', {
        'service': service,
        'parametros': parametros,
        'parameters': parameters,
        'rca': rca,
        'norma': norma,
        'project': project,
    })

 
@login_required 
def edit_sample_parameter(request,parameter_id):
    """Edit sample parameter model."""
    
    parametro = models.ParametroDeMuestra.objects.get(id=parameter_id)   
    if request.method == 'POST':
        responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
        parametro.responsable_de_analisis= responsable
        parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
        parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
        parametro.resultado = request.POST['resultado']
        parametro.factor_de_dilucion = request.POST['factor_de_dilucion']
        parametro.resultado_final = request.POST['resultado_final']
        parametro.creator_user = request.POST['creator_user']
        parametro.save()
        
        servicio_id = parametro.servicio_id
        return redirect('lims:service', servicio_id)
    
    return render(request, 'lims/edit_sample_parameter.html', {
       'parameter': parametro,
    })


@login_required
def service_parameters(request):
    """Service parameters view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.exclude(ensayo__icontains='GRV').order_by('servicio_id')
    # queryset_service_parameters = models.ParametroDeMuestra.objects.all().order_by('-created')
    parametros = models.ParametroEspecifico.objects.exclude(codigo__icontains = 'GRV')
    parameters = parametros
    paginator = Paginator(queryset_service_parameters, 25)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(parametro_id=request.POST['parametro'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })


        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(codigo_servicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })


            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(fecha_de_inicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })

        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    parametro.fecha_de_inicio = row['fecha_de_inicio']
                    parametro.fecha_de_terminado = row['fecha_de_terminado']
                    parametro.peso_inicial = row['peso_inicial']
                    parametro.peso_final = row['peso_final']
                    parametro.resultado_final = round(row['resultado_final'],4)
                    parametro.responsable_de_analisis = request.POST['responsable_de_analisis']
                    parametro.save()

            return redirect('lims:service_parameters_filter')


        else:
            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
            parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            fecha_terminado = request.POST['fecha_de_terminado']
            fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
            parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            parametro.resultado = request.POST['resultado']
            parametro.factor_de_dilucion = request.POST['factor_de_dilucion']
            parametro.resultado_final = request.POST['resultado_final']
            parametro.creator_user = request.POST['creator_user']
            parametro.save()

            return redirect('lims:service_parameters')


    return render(request, 'lims/service_parameters.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
def service_parameters_filter(request):
    """Service parameters for filter view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains='GRV').order_by('servicio_id')
    # queryset_service_parameters = models.ParametroDeMuestra.objects.all().order_by('-created')
    parametros = models.ParametroEspecifico.objects.filter(codigo__icontains = 'GRV')
    parameters = parametros
    paginator = Paginator(queryset_service_parameters, 25)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(parametro_id=request.POST['parametro'])).order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })


        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })
            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(codigo_servicio__contains=request.POST['search_text'])).order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(ensayo__icontains=request.POST['search_text'])).order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(fecha_de_inicio__contains=request.POST['search_text'])).order_by('-created')
                paginator = Paginator(queryset_service_parameters, 25)
                page = request.GET.get('page')
                service_parameters = paginator.get_page(page)
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                return render(request, 'lims/service_parameters_filter.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })

        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    parametro.fecha_de_inicio = row['fecha_de_inicio']
                    parametro.fecha_de_terminado = row['fecha_de_terminado']
                    parametro.peso_inicial = row['peso_inicial']
                    parametro.peso_final = row['peso_final']
                    parametro.resultado_final = round(row['resultado_final'],4)
                    parametro.responsable_de_analisis = request.POST['responsable_de_analisis']
                    parametro.save()

            return redirect('lims:service_parameters_filter')

        else:
            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
            parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            fecha_terminado = request.POST['fecha_de_terminado']
            fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
            parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            parametro.peso_inicial = request.POST['peso_inicial']
            parametro.peso_final = request.POST['peso_final']
            parametro.resultado_final = request.POST['resultado_final']
            parametro.save()
            
           
            return redirect('lims:service_parameters_filter')


    return render(request, 'lims/service_parameters_filter.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
def projects(request):
    """Projects view."""

    queryset_proyectos = models.Proyecto.objects.all().order_by('codigo')
    clientes = models.Cliente.objects.all().order_by('titular')
    paginator = Paginator(queryset_proyectos, 25)
    page = request.GET.get('page')
    proyectos = paginator.get_page(page)
    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                return render(request, 'LIMS/projects.html',{
                    'proyectos': proyectos,
                    'clientes': clientes,
                })
            else:
                queryset_proyectos = models.Proyecto.objects.filter(cliente_id=request.POST['client']).order_by('codigo')
                paginator = Paginator(queryset_proyectos, 25)
                page = request.GET.get('page')
                proyectos = paginator.get_page(page)
                return render(request, 'LIMS/projects.html',{
                    'proyectos': proyectos,
                    'clientes': clientes,
                })

        if 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                return render(request, 'LIMS/projects.html',{
                    'proyectos': proyectos,
                    'clientes': clientes,
                })

            if request.POST['opcion'] == 'codigo':
                queryset_proyectos = models.Proyecto.objects.filter(codigo__contains=request.POST['search_text']).order_by('codigo')
                paginator = Paginator(queryset_proyectos, 25)
                page = request.GET.get('page')
                proyectos = paginator.get_page(page)
                return render(request, 'LIMS/projects.html',{
                    'proyectos': proyectos,
                    'clientes': clientes,
                })

            if request.POST['opcion'] == 'nombre':
                queryset_proyectos = models.Proyecto.objects.filter(nombre__icontains=request.POST['search_text']).order_by('codigo')
                paginator = Paginator(queryset_proyectos, 25)
                page = request.GET.get('page')
                proyectos = paginator.get_page(page)
                return render(request, 'LIMS/projects.html',{
                    'proyectos': proyectos,
                    'clientes': clientes,
                })

    return render(request, 'LIMS/projects.html',{
        'proyectos': proyectos,
        'clientes': clientes,
    })


@login_required
def services(request):
    """Services view."""

    queryset_servicios = models.Servicio.objects.all().order_by('-created')
    clientes = models.Cliente.objects.all().order_by('titular')
    paginator = Paginator(queryset_servicios, 25)
    page = request.GET.get('page')
    servicios = paginator.get_page(page)
    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

            else:
                queryset_servicios = models.Servicio.objects.filter(cliente=request.POST['client']).order_by('-created')
                paginator = Paginator(queryset_servicios, 25)
                page = request.GET.get('page')
                servicios = paginator.get_page(page)
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

        elif 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

            if request.POST['opcion'] == 'codigo':
                queryset_servicios = models.Servicio.objects.filter(codigo_muestra__contains=request.POST['search_text']).order_by('-created')
                paginator = Paginator(queryset_servicios, 25)
                page = request.GET.get('page')
                servicios = paginator.get_page(page)
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

            if request.POST['opcion'] == 'punto':
                queryset_servicios = models.Servicio.objects.filter(punto_de_muestreo__icontains=request.POST['search_text']).order_by('-created')
                paginator = Paginator(queryset_servicios, 25)
                page = request.GET.get('page')
                servicios = paginator.get_page(page)
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

            if request.POST['opcion'] == 'muestreo':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_muestreo__contains=request.POST['search_text']).order_by('-created')
                paginator = Paginator(queryset_servicios, 25)
                page = request.GET.get('page')
                servicios = paginator.get_page(page)
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })
            
            if request.POST['opcion'] == 'recepcion':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_recepcion__contains=request.POST['search_text']).order_by('-created')
                paginator = Paginator(queryset_servicios, 25)
                page = request.GET.get('page')
                servicios = paginator.get_page(page)
                return render(request, 'LIMS/services.html',{
                    'servicios': servicios,
                    'clientes': clientes,
                })

        else:
            
            servicio = models.Servicio.objects.get(codigo_muestra=request.POST['servicio_id'])
            servicio.responsable = request.POST['responsable']
            fecha_muestreo = request.POST['fecha_de_muestreo']
            fecha_de_muestreo = datetime.strptime(fecha_muestreo, "%d-%m-%Y")
            servicio.fecha_de_muestreo = fecha_de_muestreo.strftime("%Y-%m-%d")
            fecha_recepcion = request.POST['fecha_de_recepcion']
            fecha_de_recepcion = datetime.strptime(fecha_recepcion, "%d-%m-%Y")
            servicio.fecha_de_recepcion = fecha_de_recepcion.strftime("%Y-%m-%d")
            servicio.save()
            
           
            return redirect('lims:services')
            
    return render(request, 'LIMS/services.html',{
        'servicios': servicios,
        'clientes': clientes,
    })


@login_required
def edit_sample_code(request, service_id):
    """Edit sample code view."""

    service = models.Servicio.objects.get(pk= service_id)
    parameters = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    try:
        if request.method == 'POST':
            codigo_muestra = request.POST['codigo_muestra']
            service.codigo_muestra = codigo_muestra
            service.editor_sample_code = request.POST['edit_code']
            service.save()

            for parameter in parameters:
                parameter.codigo_servicio = codigo_muestra
                parameter.save()

            return redirect('lims:services')
    except:
        error = 'El código de muestra ya existe.'
        return render(request, 'LIMS/edit_service_code.html', {
        'service': service,
        'error': error,
    })


    return render(request, 'LIMS/edit_service_code.html', {
        'service': service,
    })