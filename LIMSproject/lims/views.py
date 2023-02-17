"""LIMS views."""
# Djnago module
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q

from . import models, forms
from datetime import datetime
from workdays import workday

# Pandas module
import pandas as pd

# Bokeh module
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral
from bokeh.models import ColumnDataSource
# Create your views here.

def is_lab(user):
    return user.groups.filter(name='laboratorio').exists()

def is_manager(user):
    return user.groups.filter(name='manager').exists()

def is_commercial(user):
    return user.groups.filter(name='comercial').exists()

def is_income(user):
    return user.groups.filter(name='ingreso').exists()

def is_income_or_coordinador(user):
    return user.groups.filter(name='ingreso').exists() or user.groups.filter(name='coordinador').exists()

def is_commercial_or_income(user):
    return user.groups.filter(name='comercial').exists() or user.groups.filter(name='ingreso').exists() or user.groups.filter(name='coordinador').exists()

def is_analyst(user):
    return user.groups.filter(name='analista').exists()

def is_coordinador(user):
    return user.groups.filter(name='coordinador').exists()

def add_workdays(start_date, num_workdays):
    end_date = workday(start_date, num_workdays)
    return end_date


def list_to_string(lista):
    if len(lista)==2:
        return ' y '.join(lista)
    else:
        return ', '.join(lista)


def render_view(request, template, context):
    """Render views"""
    return render(request, template, context)


@login_required
@user_passes_test(is_lab)
def index(request):
    """Index view."""
    return render(request, 'LIMS/menu.html')


@login_required
@user_passes_test(is_commercial,login_url='lims:index')
def clients(request):
    """Clients view."""

    clientes = models.Cliente.objects.all().order_by('titular')
    paginator = Paginator(clientes, 25)
    page = request.GET.get('page')
    clients = paginator.get_page(page)
    template = 'LIMS/clients.html'

    if request.method == 'POST':
        if request.POST['search_text'] == '' or request.POST['opcion'] == '':
            context = {
                'clients': clients,
                }
            return render_view(request, template, context)
        elif request.POST['opcion'] == 'titular':
            clientes = models.Cliente.objects.filter(titular__icontains = request.POST['search_text']).order_by('titular')
            paginator = Paginator(clientes, 25)
            page = request.GET.get('page')
            clients = paginator.get_page(page)
            context = {
                'clients': clients,
                }
            return render_view(request, template, context)


        elif request.POST['opcion'] == 'rut':
            clientes = models.Cliente.objects.filter(rut__contains = request.POST['search_text']).order_by('titular')
            paginator = Paginator(clientes, 25)
            page = request.GET.get('page')
            clients = paginator.get_page(page)
            context = {
                'clients': clients,
                }
            return render_view(request, template, context)
    
    
    context = {
                'clients': clients,
                }
    return render_view(request, template, context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
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
@user_passes_test(is_commercial, login_url='lims:index')
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

    queryset_projects = models.Proyecto.objects.filter(cliente_id = id_cliente).order_by('-created')
    paginator_projects = Paginator(queryset_projects, 5)
    page_project = request.GET.get('page_project')
    projects = paginator_projects.get_page(page_project)
    template = 'LIMS/client.html'
    context = {
        'cliente':cliente,
        'contacts': contacts,
        'sample_points':sample_points,
        'legal_representatives': legal_representatives,
        'rcas': rcas,
        'projects': projects,
    }
    return render_view(request, template, context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_legal_representative(request, id_cliente):
    """Client add legal representative view."""

    template = 'LIMS/client_add_legal_representative.html'
    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                context = {
                    'pm':pm,
                    'len_pm': len_pm,
                    }
                if len_pm != 1:
                    return render_view(request, template, context)
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
                    rut=rut.replace('-','').replace('.','').replace(',',''), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                context = {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                }
                return render_view(request, template, context)
            else:
                return redirect('lims:client', id_cliente)
    context = {
        'pm':[0],
        'len_pm': 1,
    }
    return render_view(request, template, context )


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_contact(request, id_cliente):
    """Client add contact view."""

    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/client_add_contact.html', {
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
                    rut=rut.replace('-','').replace('.','').replace(',',''), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                return render(request, 'LIMS/client_add_contact.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:client', id_cliente)
    return render(request, 'LIMS/client_add_contact.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_sample_point(request, id_cliente):
    '''Client add sample point view.'''

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/client_add_sample_point.html', {
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
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_rca(request, id_cliente):
    '''Client add RCA view.'''

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/client_add_rca.html', {
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
@user_passes_test(is_commercial, login_url='lims:index')
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


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
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


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_project_cot_etfa(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    parameters = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo')
    
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
@user_passes_test(is_manager, login_url='lims:index')
def normas_ref(request):
    """Normas de referencias view."""

    queryset_normas = models.NormaDeReferencia.objects.all().order_by('norma')
    paginator = Paginator(queryset_normas, 25)
    page = request.GET.get('page')
    normas = paginator.get_page(page)

    if request.method == 'POST':
        if 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            print(df)

            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            
            for index, row in df.iterrows():
                if   models.NormaDeReferencia.objects.filter(norma=row['Norma']).exists():
                    continue
                else:
                    models.NormaDeReferencia.objects.create(norma = row['Norma'], descripcion= row['Descripción'],creator_user = responsable_de_analisis)
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return render(request, 'LIMS/normas_ref.html',{
        'normas': normas,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_normas_ref(request):
    """Add Standards of reference view."""

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/add_normas_ref.html', {
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
@user_passes_test(is_manager, login_url='lims:index')
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
@user_passes_test(is_manager, login_url='lims:index')
def add_method(request):
    """Add method view."""

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/add_method.html', {
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

                return render(request, 'LIMS/add_method.html', {
                    'pm':[0],
                    'len_pm': 1,
                    'error_duplicados': error_duplicados,
                })
            else:
                return redirect('lims:methods')

    
    return render(request, 'LIMS/add_method.html', {
        'pm':[0],
        'len_pm': 1,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
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
@user_passes_test(is_manager, login_url='lims:index')
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
@user_passes_test(is_manager, login_url='lims:index')
def parameters(request):
    '''Parameters view.'''

    metodos = models.Metodo.objects.all()
    queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo', 'codigo')
   
    if request.method == 'POST':
        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')

            if request.POST['buscar'] == 'ensayo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(ensayo__icontains=request.POST['search_text']).order_by('ensayo')

            if request.POST['buscar'] == 'codigo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(codigo__icontains=request.POST['search_text']).order_by('ensayo')

            if request.POST['buscar'] == 'metodo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(metodo__icontains=request.POST['search_text']).order_by('ensayo')
                
    paginator = Paginator(queryset_parameters, 35)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    return render(request, 'LIMS/parameters.html', {
        'parameters': parameters,
        'metodos': metodos,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
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
            return render(request, 'LIMS/add_parameter.html',{
                'metodos': metodos,
                'tipos_de_muestras': tipos_de_muestras,
                'error_parameter': error,
            })

    return render(request, 'LIMS/add_parameter.html',{
        'metodos': metodos,
        'tipos_de_muestras': tipos_de_muestras,
    })
    


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def samples_type(request):
    """Samples type view."""

    queryset_samples_type = models.TipoDeMuestra.objects.all().order_by('nombre')
    paginator = Paginator(queryset_samples_type, 35)
    page = request.GET.get('page')
    samples_type = paginator.get_page(page)
    
    return render(request, 'LIMS/samples_type.html', {
        'samples_type':samples_type,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_sample_type(request):
    """Add Standards of reference view."""

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    return render(request, 'LIMS/add_sample_type.html', {
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
@user_passes_test(is_manager, login_url='lims:index')
def etfa(request):
    """ETFA view."""

    queryset_services = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('codigo_etfa')
    paginator = Paginator(queryset_services, 35)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    return render(request, 'LIMS/etfa.html',{
        'services':services,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_etfa(request):
    """Add ETFA view."""

    parameters = models.ParametroEspecifico.objects.filter(codigo_etfa = None).order_by('ensayo')
    
    if request.method == 'POST':
        parametro = models.ParametroEspecifico.objects.get(id=request.POST['parametro'])
        parametro.codigo_etfa = request.POST['codigo']
        parametro.save()
        return redirect('lims:etfa')

    return  render(request, 'LIMS/add_etfa.html', {
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def delete_etfa(request, parameter_id):
    parameter = models.ParametroEspecifico.objects.get(id=parameter_id)
    parameter.codigo_etfa = None
    parameter.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
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
    
    return render(request, 'LIMS/project.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'services': services,
        'parameters': parameters_service,
    })


@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
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
    
    return render(request, 'LIMS/project_cot.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'services': services,
        'parameters': parameters_service,
        'parametros_cotizados':parametros_cotizados,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:project')
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

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif last_service.codigo_muestra[-2:] != current_year: 
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
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
                    created = datetime.now()
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_service.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:project')
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

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif last_service.codigo_muestra[-2:] != current_year: 
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
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
                    created = datetime.now()
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_service_etfa.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:project_cot')
def clone_service(request, service_id):
    """Clone service view."""

    service = models.Servicio.objects.get(pk = service_id)
    proyectos = models.Proyecto.objects.filter(cliente_id = service.proyecto.cliente)
    parameters = models.ParametroDeMuestra.objects.filter(codigo_servicio = service.codigo_muestra)
    parameters = [p.parametro_id for p in parameters]
    rcas = models.RCACliente.objects.filter(cliente_id = service.proyecto.cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id= service.proyecto.cliente)
    normas = models.NormaDeReferencia.objects.all()
    tipos_de_muestras = models.TipoDeMuestra.objects.all()

    context = {
        'service': service,
        'proyectos': proyectos,
        'parameters': parameters,
        'rcas': rcas,
        'normas': normas,
        'sample_points': sample_points,
        'tipos_de_muestras': tipos_de_muestras,
    }

    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        project = models.Proyecto.objects.get(pk = proyecto)

        parameters_cot = project.parametros_cotizados.all()
        parameters_cot = [p.id for p  in parameters_cot]

        def comprobador_de_parametros(parameters=parameters, parameters_cot= parameters_cot):
            for p in parameters:
                if p not in parameters_cot:
                    return False
                else: continue
            return True

        punto_de_muestreo = request.POST['punto_de_muestreo']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        fecha_de_contenedores = request.POST['fecha_de_contenedores']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        
        fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]

        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif last_service.codigo_muestra[-2:] != current_year: 
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'

 
        if len(parameters_cot)==0 or comprobador_de_parametros():
            for sp in sample_points:
                if int(punto_de_muestreo) == int(sp.id):   
                    models.Servicio.objects.create(
                        codigo = codigo_de_servicio,
                        codigo_muestra = codigo_generado, 
                        proyecto_id = proyecto, 
                        punto_de_muestreo = sp.nombre,
                        tipo_de_muestra = service.tipo_de_muestra,
                        fecha_de_muestreo = fecha_de_muestreo,
                        observacion = observacion,
                        fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                        fecha_de_contenedores = fecha_de_contenedores,
                        norma_de_referencia = norma_de_referencia,
                        rCA = rCA,
                        etfa = service.etfa,
                        muestreado_por_algoritmo = muestreado_por_algoritmo,
                        creator_user = creator_user,
                        cliente = service.cliente,
                        created = datetime.now()
                        )                    

            for pid in parameters:
                ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                models.ParametroDeMuestra(
                    servicio_id = codigo_de_servicio, 
                    parametro_id= pid,
                    ensayo= ensayo.codigo, 
                    codigo_servicio= codigo_generado,
                    creator_user = creator_user,
                    created = datetime.now()
                    ).save()

            return redirect('lims:project', service.proyecto_id)

        else:
            error = 'No se pudo clonar el servicio debido a que algún parámetro no se encuentra entre los cotizados para el proyecto seleccionado.'
            context['error'] = error


    return render(request, "LIMS/clone_service.html", context)


@login_required
@user_passes_test(is_income, login_url='lims:project_cot')
def add_service_cot(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    parametros_cot = project.parametros_cotizados.all()
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
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

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        elif last_service.codigo_muestra[-2:] != current_year: 
            codigo_central = ('1').zfill(5)
            codigo_generado = f'{codigo_central}-{current_year}'
        
        elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
            codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'

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
                    created = datetime.now()
                    )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_service_cot.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'normas': normas,
        'parametros_cot': parametros_cot,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
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
                creator_user=creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'LIMS/add_service_parameter.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
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
                creator_user=creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'LIMS/add_service_parameter_etfa.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
def service(request, service_id):
    """Service view."""

    service = models.Servicio.objects.get(pk=service_id)
    client = models.Cliente.objects.get(pk=service.cliente)
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    queryset_parameters = models.ParametroDeMuestra.objects.filter(servicio_id=service_id).order_by('-created')
    paginator = Paginator(queryset_parameters, 10)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    rca = models.RCACliente.objects.get(pk=service.rCA)
    norma = models.NormaDeReferencia.objects.get(pk=service.norma_de_referencia)
    project = models.Proyecto.objects.get(pk=service.proyecto_id)
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    comercial = user.groups.filter(name='comercial').exists()
    
    def prog():
        progreso = 0
        for p in queryset_parameters:
            if p.resultado_final!=None: 
                progreso+=1
        analizado = progreso
        return analizado, (progreso/len(queryset_parameters))*100

    analizado, progreso  = prog()

    return render(request, 'LIMS/service.html', {
        'service': service,
        'client': client,
        'parametros': parametros,
        'parameters': parameters,
        'rca': rca,
        'norma': norma,
        'project': project,
        'manager': manager,
        'progreso': progreso,
        'total': len(queryset_parameters),
        'analizado': analizado,
        'comercial': comercial,
    })

 
@login_required 
@user_passes_test(is_manager, login_url='lims:index')
def edit_sample_parameter(request,parameter_id):
    """Edit sample parameter model."""
    
    parametro = models.ParametroDeMuestra.objects.get(id=parameter_id)   
    verify = 'GRV' in parametro.ensayo
    if request.method == 'POST':
        responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
        parametro.responsable_de_analisis= responsable
        parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
        parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
        
        if verify:
            parametro.peso_inicial = float(request.POST['peso_inicial'].replace(',','.'))
            parametro.peso_final = float(request.POST['peso_final'].replace(',','.'))
        else:
            parametro.resultado = float(request.POST['resultado'].replace(',','.'))
            parametro.factor_de_dilucion = float(request.POST['factor_de_dilucion'].replace(',','.'))
        
        parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
        parametro.creator_user = request.POST['creator_user']
        parametro.save()
        
        servicio_id = parametro.servicio_id
        return redirect('lims:service', servicio_id)
    
    return render(request, 'LIMS/edit_sample_parameter.html', {
       'parameter': parametro,
       'verify': verify,
    })


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def service_parameters(request):
    """Service parameters view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.exclude(ensayo__icontains='GRV').order_by('-created')
    parametros = models.ParametroEspecifico.objects.exclude(codigo__icontains = 'GRV')
    parameters = parametros

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(parametro_id=request.POST['parametro'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(codigo_servicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(fecha_de_inicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

        elif 'fecha_de_inicio' in request.POST.keys():
            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.resultado = float(request.POST['resultado'].replace(',','.'))
            parametro.factor_de_dilucion = float(request.POST['factor_de_dilucion'].replace(',','.'))
            parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
            parametro.save()

            return redirect('lims:service_parameters')

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    if parametro.resultado_final == None:
                        parametro.fecha_de_inicio = row['fecha_de_inicio']
                        parametro.fecha_de_terminado = row['fecha_de_terminado']
                        parametro.resultado = row['resultado']
                        parametro.factor_de_dilucion = row['factor_de_dilucion']
                        parametro.resultado_final = round(row['resultado_final'],4)
                        parametro.responsable_de_analisis = responsable_de_analisis
                        parametro.save()
                    else: continue

            return redirect('lims:service_parameters')

    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/service_parameters.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def service_parameters_filter(request):
    """Service parameters for filter view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains='GRV').order_by('-created')
    parametros = models.ParametroEspecifico.objects.filter(codigo__icontains = 'GRV')
    parameters = parametros
    

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(parametro_id=request.POST['parametro'])).order_by('-created')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(codigo_servicio__contains=request.POST['search_text'])).order_by('-created')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(ensayo__icontains=request.POST['search_text'])).order_by('-created')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(fecha_de_inicio__contains=request.POST['search_text'])).order_by('-created')

        elif 'fecha_de_inicio' in request.POST.keys():

            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.peso_inicial = float(request.POST['peso_inicial'].replace(',','.'))
            parametro.peso_final = float(request.POST['peso_final'].replace(',','.'))
            parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
            parametro.save()
           
            return redirect('lims:service_parameters_filter')

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass

        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    if parametro.resultado_final == None:
                        parametro.fecha_de_inicio = row['fecha_de_inicio']
                        parametro.fecha_de_terminado = row['fecha_de_terminado']
                        parametro.peso_inicial = row['peso_inicial']
                        parametro.peso_final = row['peso_final']
                        parametro.resultado_final = round(row['resultado_final'],4)
                        parametro.responsable_de_analisis = responsable_de_analisis
                        parametro.save()
                    else: continue 

            return redirect('lims:service_parameters_filter')
    
    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/service_parameters_filter.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def service_parameter_dropped(request, parameter_id):
    parameter = models.ParametroDeMuestra.objects.get(id = parameter_id)

    models.ParametroDeMuestraDescartada.objects.create(
        servicio = parameter.servicio,
        batch = parameter.batch,
        codigo_servicio = parameter.codigo_servicio,
        parametro = parameter.parametro,
        responsable_de_analisis= parameter.responsable_de_analisis,
        fecha_de_inicio = parameter.fecha_de_inicio,
        fecha_de_terminado = parameter.fecha_de_terminado,
        resultado = parameter.resultado,
        factor_de_dilucion = parameter.factor_de_dilucion,
        resultado_final = parameter.resultado_final,
        peso_inicial = parameter.peso_inicial,
        peso_final = parameter.peso_final,
        ensayo = parameter.ensayo,
        created = parameter.created,
        discarder = request.user.username,
        creator_user = parameter.creator_user,
        )

    parameter.responsable_de_analisis = None
    parameter.fecha_de_inicio = None
    parameter.fecha_de_terminado = None
    parameter.resultado = None
    parameter.factor_de_dilucion = None
    parameter.peso_inicial = None
    parameter.peso_final = None
    parameter.resultado_final = None
    parameter.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@user_passes_test(is_manager, 'lims:index')
def discarded_service_parameters(request):
    """Discarded service parameters view."""

    queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.exclude(ensayo__icontains='GRV').order_by('-discarded')
    parametros = models.ParametroEspecifico.objects.exclude(codigo__icontains = 'GRV')
    parameters = parametros

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(parametro_id=request.POST['parametro'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(codigo_servicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(ensayo__icontains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(fecha_de_inicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

    paginator = Paginator(queryset_service_parameters,35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/discarded_service_parameters.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def discarded_service_parameters_filter(request):
    """Service parameters for filter view."""

    queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(ensayo__icontains='GRV').order_by('-discarded')
    parametros = models.ParametroEspecifico.objects.filter(codigo__icontains = 'GRV')
    parameters = parametros
    

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(parametro_id=request.POST['parametro'])).order_by('-discarded')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(codigo_servicio__contains=request.POST['search_text'])).order_by('-discarded')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(ensayo__icontains=request.POST['search_text'])).order_by('-discarded')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(fecha_de_inicio__contains=request.POST['search_text'])).order_by('-discarded')
    
    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/discarded_service_parameters_filter.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })

@login_required
@user_passes_test(is_manager, login_url='lims:index')
def projects(request):
    """Projects view."""

    queryset_proyectos = models.Proyecto.objects.all().order_by('codigo')
    clientes = models.Cliente.objects.all().order_by('titular')
    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                pass
            else:
                queryset_proyectos = models.Proyecto.objects.filter(cliente_id=request.POST['client']).order_by('codigo')


        if 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                pass

            if request.POST['opcion'] == 'codigo':
                queryset_proyectos = models.Proyecto.objects.filter(codigo__contains=request.POST['search_text']).order_by('codigo')


            if request.POST['opcion'] == 'nombre':
                queryset_proyectos = models.Proyecto.objects.filter(nombre__icontains=request.POST['search_text']).order_by('codigo')

    paginator = Paginator(queryset_proyectos, 35)
    page = request.GET.get('page')
    proyectos = paginator.get_page(page)
    return render(request, 'LIMS/projects.html',{
        'proyectos': proyectos,
        'clientes': clientes,
    })


@login_required
@user_passes_test(is_income_or_coordinador, login_url='lims:index')
def services(request):
    """Services view."""

    queryset_servicios = models.Servicio.objects.all().order_by('-created')
    clientes = models.Cliente.objects.all().order_by('titular')

    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                pass

            else:
                queryset_servicios = models.Servicio.objects.filter(cliente=request.POST['client']).order_by('-created')


        elif 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                pass

            if request.POST['opcion'] == 'codigo':
                queryset_servicios = models.Servicio.objects.filter(codigo_muestra__contains=request.POST['search_text']).order_by('-created')


            if request.POST['opcion'] == 'punto':
                queryset_servicios = models.Servicio.objects.filter(punto_de_muestreo__icontains=request.POST['search_text']).order_by('-created')


            if request.POST['opcion'] == 'muestreo':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_muestreo__contains=request.POST['search_text']).order_by('-created')

            
            if request.POST['opcion'] == 'recepcion':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_recepcion__contains=request.POST['search_text']).order_by('-created')


        else:
            servicio = models.Servicio.objects.get(codigo_muestra=request.POST['servicio_id'])
            servicio.responsable = request.POST['responsable']
            fecha_muestreo = request.POST['fecha_de_muestreo']
            fecha_de_muestreo = datetime.strptime(fecha_muestreo, "%d-%m-%Y")
            servicio.fecha_de_muestreo = fecha_de_muestreo.strftime("%Y-%m-%d")
            fecha_recepcion = request.POST['fecha_de_recepcion']
            if fecha_recepcion.endswith(str(datetime.now().year)):
                fecha_de_recepcion = datetime.strptime(fecha_recepcion, "%d-%m-%Y")
                servicio.fecha_de_recepcion = fecha_de_recepcion.strftime("%Y-%m-%d")
            else: servicio.fecha_de_recepcion = request.POST['fecha_de_recepcion']
            servicio.save()
            
           
            return redirect('lims:services')

    paginator = Paginator(queryset_servicios, 35)
    page = request.GET.get('page')
    servicios = paginator.get_page(page)            
    return render(request, 'LIMS/services.html',{
        'servicios': servicios,
        'clientes': clientes,
    })


@login_required
@user_passes_test(is_income, login_url='lims:index')
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


@login_required
def export_data_to_excel(request, username):
    """Export data to excel view."""
    usuario = User.objects.get(username = username)
    clave = models.Cliente.objects.get(titular=User.objects.get(username = usuario.username).first_name).id
    parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id__cliente_id__pk = clave)
    parametros = parametros.select_related('servicio').all()
    parametros = parametros.select_related('parametro').all().order_by('-codigo_servicio')
    
    data = [
        {
        'ID Muestra':parametro.codigo_servicio,
        'Descripción':parametro.servicio.punto_de_muestreo,
        'Fecha de muestreo': parametro.servicio.fecha_de_muestreo,
        'Fecha de recepción': parametro.servicio.fecha_de_recepcion,
        'Parametro': parametro.ensayo,
        'Unidad': parametro.parametro.unidad,
        'Resultado': parametro.resultado_final
        }
        for parametro in parametros
    ]
    
    df = pd.DataFrame.from_records(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data_algoritmos.xlsx'
    df.to_excel(response, index=False)
    return response
    

@login_required
def project_client(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk = project.cliente_id)
    queryset_parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id = project_id)
    queryset_parametros = queryset_parametros.select_related('servicio').all()
    queryset_parametros = queryset_parametros.select_related('parametro').all().order_by('-codigo_servicio')
    paginator = Paginator(queryset_parametros, 20)
    page = request.GET.get('page')
    parametros = paginator.get_page(page)

    if request.method == 'POST':
        if request.POST['search_text'] == '' or request.POST['buscar'] == '':
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'servicio':
            queryset_parametros = queryset_parametros.filter(codigo_servicio__contains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'ensayo':
            queryset_parametros = queryset_parametros.filter(ensayo__icontains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'muestreo':
            queryset_parametros = queryset_parametros.filter(servicio__fecha_de_muestreo__contains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })
        
        elif request.POST['buscar'] == 'punto':
            queryset_parametros = queryset_parametros.filter(servicio__punto_de_muestreo__icontains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })



    return render(request, 'LIMS/client_analysis.html', {
        'project': project, 
        'cliente': cliente,
        'parametros': parametros,
    })


@login_required
def export_data_project_to_excel(request, project_id):
    """Export data to excel view."""
    parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id = project_id)
    parametros = parametros.select_related('servicio').all()
    parametros = parametros.select_related('parametro').all().order_by('-codigo_servicio')
    
    data = [
        {
        'ID Muestra':parametro.codigo_servicio,
        'Descripción':parametro.servicio.punto_de_muestreo,
        'Fecha de muestreo': parametro.servicio.fecha_de_muestreo,
        'Fecha de recepción': parametro.servicio.fecha_de_recepcion,
        'Parametro': parametro.ensayo,
        'Unidad': parametro.parametro.unidad,
        'Resultado': parametro.resultado_final
        }
        for parametro in parametros
    ]
    
    df = pd.DataFrame.from_records(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data_algoritmos.xlsx'
    df.to_excel(response, index=False)
    return response


@login_required
def grafico(request, service_id):
    """vista para graficar."""
    parametros = models.ParametroDeMuestra.objects.filter(codigo_servicio=service_id)
    parametros_x = [p.ensayo for p in parametros]
    resultados_y = [0 if p.resultado_final == None else 1 for p in parametros]

    source = ColumnDataSource(data=dict(parametros_x=parametros_x, resultados_y=resultados_y))
    
    plot = figure(
        x_range=parametros_x, 
        y_range=(0,1.1), 
        height=350,
        toolbar_location=None, 
        tools=""
        )

    plot.vbar(x='parametros_x', top='resultados_y', width=0.9, source=source)
   
    script, div = components(plot)

    return render(request, 'LIMS/service_chart.html', {
        'script': script, 
        'div': div
        })

@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def batches(request):
    """Batches view."""
    queryset_batches = models.Batch.objects.all().order_by("-created")
   
    services = models.ParametroDeMuestra.objects.select_related('batch').order_by('-created')
    user = request.user
    coordinador = user.groups.filter(name='coordinador').exists()

    if request.method == 'POST':
        text = request.POST['search_text']
        opcion = request.POST['opcion']
        if text=='' or opcion == '':
            pass
        elif opcion == 'codigo':
            queryset_batches = queryset_batches.filter(codigo__icontains = text)
        elif opcion == 'responsable':
            queryset_batches = queryset_batches.filter(responsable__icontains = text)
        elif opcion == 'parametro':
            queryset_batches = queryset_batches.filter(parametro__icontains= text)
    
    paginator = Paginator(queryset_batches, 35)
    page = request.GET.get('page')
    lotes = paginator.get_page(page)
    return render(request, "LIMS/batches.html", {
        'lotes': lotes,
        'services': services,
        'coordinador': coordinador,
    })

@login_required
@user_passes_test(is_coordinador, login_url='lims:index')
def add_batch(request):
    """Add batch view."""
    parametros = models.ParametroEspecifico.objects.all().order_by('codigo')
    servicios = models.ParametroDeMuestra.objects.select_related('parametro').filter(Q(resultado_final=None) & Q(batch_id=None)).order_by("-created")
    group = Group.objects.get(name='analista')
    analistas = User.objects.filter(groups = group).order_by('username')
    if request.method == 'POST':
        if 'parametro' in request.POST:
            if request.POST['parametro']=='':
                return render(request, "LIMS/add_batch.html", {
                    'servicios': servicios,
                    'parametros': parametros,
                    'analistas': analistas,
                })

            servicios = models.ParametroDeMuestra.objects.select_related('parametro').filter(Q(resultado_final=None) & Q(batch_id=None)).order_by("-created")
            servicios = servicios.filter(parametro__codigo = request.POST['parametro'])
            return render(request, "LIMS/add_batch.html", {
                    'servicios': servicios,
                    'parametros': parametros,
                    'analistas': analistas,
                    'parametro': request.POST['parametro'],
                })
        else: 
            current_year = datetime.now().year
            current_year = str(current_year)[2:]
            last_batch = models.Batch.objects.all().latest('codigo')
            if models.Batch.objects.exists()==False:
                codigo_de_batch = ('1').zfill(5)
                codigo_generado = f'L-{codigo_de_batch}-{current_year}'
            
            elif last_batch.codigo[-2:] != current_year:
                codigo_central = ('1').zfill(5)
                codigo_generado = f'L-{codigo_central}-{current_year}'

            elif models.Batch.objects.exists()==True and last_batch.codigo[-2:] == current_year:
                last_batch = models.Batch.objects.filter(codigo__endswith = '-'+current_year).latest('codigo')
                codigo_de_batch = str(int(last_batch.codigo[-7:-3]) +1).zfill(5)
                codigo_generado = f'L-{codigo_de_batch}-{current_year}'
            

            services = request.POST.getlist('service')
            batch = models.Batch.objects.create(
                codigo = codigo_generado, 
                parametro = request.POST['parametro_escogido'], 
                responsable_asignado_id = request.POST['analista'],
                responsable= User.objects.get(id = request.POST['analista']).username, 
                creator_user= request.POST['creator_user'])
            for service in services:
                parameter = models.ParametroDeMuestra.objects.get(id=service)
                parameter.batch = batch
                parameter.save()
            
            return redirect('lims:batches')

    return render(request, "LIMS/add_batch.html", {
        'servicios': servicios,
        'parametros': parametros,
        'analistas': analistas,
    })


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def batch(request, batch_id):
    lote = models.Batch.objects.get(codigo = batch_id)
    parametros = models.ParametroDeMuestra.objects.filter(batch_id = lote).exclude(ensayo__icontains='GRV').order_by('servicio_id')
    service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains='GRV').order_by('servicio_id')

    if request.method == 'POST':            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.resultado = request.POST['resultado']
            parametro.factor_de_dilucion = request.POST['factor_de_dilucion']
            parametro.resultado_final = request.POST['resultado_final']
            parametro.save()

            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "LIMS/batch_service_parameters.html", {
        'lote': lote,
        'parametros': parametros,
        'service_parameter': service_parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def base_importation(request):
    if request.method == 'POST':
        if 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.TipoDeMuestra.objects.filter(nombre=row['Matriz']).exists():
                    continue
                else:
                    models.TipoDeMuestra.objects.create(nombre=row['Matriz'], creator_user = responsable_de_analisis)

            for index, row in df.iterrows():
                if   models.Metodo.objects.filter(nombre=row['Código de Metodología']).exists():
                    continue
                else:
                    models.Metodo.objects.create(nombre = row['Código de Metodología'], descripcion= row['Metodología'],creator_user = responsable_de_analisis)
            
            for index, row in df.iterrows():
                if   models.ParametroEspecifico.objects.filter(codigo=row['Código de Parámetro']).exists():
                    continue
                else:
                    if row['LDM']>=0: ldm = row['LDM']
                    else: ldm = '-'
                    
                    if row['LCM']>=0: lcm = row['LCM']
                    else: lcm = '-'

                    if ldm != '-' and lcm != '-':
                        ldm_str = str(ldm)
                        int_part, dec_part = ldm_str.split('.')
                        lcm = round(lcm, len(dec_part))


                    models.ParametroEspecifico.objects.create(
                        ensayo = row['Parámetro'] , 
                        codigo= row['Código de Parámetro'], 
                        metodo = row['Código de Metodología'],
                        LDM = ldm,
                        LCM = lcm,
                        unidad = row['Unidad'],
                        tipo_de_muestra = row['Matriz'],
                        codigo_etfa = row['Código Autorización ETFA'],
                        acreditado = row['Acreditado'],
                        creator_user = responsable_de_analisis)

            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'LIMS/base_importation.html')