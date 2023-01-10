"""LIMS views."""

from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . import models, forms

# Create your views here.

@login_required
def index(request):
    """Index view."""
    return render(request, 'base/base.html')


@login_required
def clients(request):
    """Clients view."""
    
    clients = models.Cliente.objects.all().order_by('titular')
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
        models.Cliente.objects.create(
            titular=titular, 
            rut=rut, 
            direccion=direccion, 
            actividad=actividad, 
            creator_user=usuario
            )

        return redirect('lims:clients')
    return render(request, 'LIMS/add_client.html')


@login_required
def client(request, id_cliente):
    """Client model."""
    cliente = models.Cliente.objects.get(id=id_cliente)
    contacts = models.ContactoCliente.objects.filter(cliente_id = id_cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente).order_by('nombre')
    legal_representatives = models.RepresentanteLegalCliente.objects.filter(cliente_id = id_cliente).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id = id_cliente).order_by('rca_asociada')
    projects = models.Proyecto.objects.filter(cliente_id = id_cliente).order_by('codigo')
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
                models.RepresentanteLegalCliente.objects.create(
                    nombre= contacto, 
                    rut=rut, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
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
                models.ContactoCliente.objects.create(
                    nombre= contacto, 
                    rut=rut, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
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
            print(request.POST)
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            print(puntos)
            usuarios = todo[2::2]
            print(usuarios)
            for punto, usuario in zip(puntos, usuarios):
                models.PuntoDeMuestreo.objects.create(
                    nombre= punto, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
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
            for punto, usuario in zip(puntos, usuarios):
                models.RCACliente.objects.create(
                    rca_asociada= punto, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
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
       form = forms.ProjectForm(request.POST)
       if form.is_valid():
        form.save()
        return redirect('lims:client', id_cliente)
    
    return render(request, 'LIMS/client_add_project.html', {
        'sample_points' : sample_points,
        'rcas': rcas,
        'normas': normas,
        'matrices': matrices,
        'cliente': cliente,
    })


@login_required
def normas_ref(request):
    """Normas de referencias view."""

    normas = models.NormaDeReferencia.objects.all().order_by('norma')
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

    metodos = models.Metodo.objects.all().order_by('nombre')
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
                models.Metodo.objects.create(
                    nombre= nombre, 
                    creator_user=usuario
                    ) 
            return redirect('lims:methods')
    return render(request, 'lims/add_method.html', {
        'pm':[0],
        'len_pm': 1,
    })

@login_required
def containers(request):
    '''Containers view.'''

    envases = models.Envase.objects.all().order_by('nombre')
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


@login_required
def parameters(request):
    '''Parameters view.'''

    parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')
    metodos = models.Metodo.objects.all()
    return render(request, 'lims/parameters.html', {
        'parameters': parameters,
        'metodos': metodos,
    })


@login_required
def add_parameter(request):

    metodos = models.Metodo.objects.all()
    tipos_de_muestras = models.TipoDeMuestra.objects.all()
    if request.method == 'POST':
        form = forms.ParameterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('lims:parameters')
    return render(request, 'lims/add_parameter.html',{
        'metodos': metodos,
        'tipos_de_muestras': tipos_de_muestras,
    })
    


@login_required
def samples_type(request):

    samples_type = models.TipoDeMuestra.objects.all().order_by('nombre')
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
            for nombre, usuario in zip(nombres, usuarios):
                models.TipoDeMuestra.objects.create(
                    nombre=nombre, 
                    creator_user=usuario
                    ) 
            return redirect('lims:samples_type')

    return render(request, 'LIMS/add_sample_type.html', {
        'pm':[0],
        'len_pm': 1,
    })

@login_required
def etfa(request):
    services = models.ETFA.objects.all().order_by('codigo')
    parameters = models.ParametroEspecifico.objects.all()
    return render(request, 'lims/etfa.html',{
        'services':services,
        'parameters': parameters,
    })


@login_required
def add_etfa(request):
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
    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id)
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id)
    services = models.Servicio.objects.filter(proyecto_id=project_id).order_by('-created')
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
def add_service(request, project_id):
    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':
        codigo_muestra = request.POST['codigo_muestra']
        proyecto = request.POST['proyecto']
        punto_de_muestreo = request.POST['punto_de_muestreo']
        tipo_de_muestra = request.POST['tipo_de_muestra']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        envases = request.POST['envases']
        fecha_de_recepcion = request.POST['fecha_de_recepcion']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        etfa = request.POST['etfa']
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        
        for sp in sample_points:
            if int(punto_de_muestreo) == int(sp.id):
                models.Servicio(
                    codigo_muestra = codigo_muestra, 
                    proyecto_id = proyecto, 
                    punto_de_muestreo = sp.nombre,
                    tipo_de_muestra = tipo_de_muestra,
                    fecha_de_muestreo = fecha_de_muestreo,
                    envases = envases,
                    fecha_de_recepción = fecha_de_recepcion,
                    norma_de_referencia = norma_de_referencia,
                    rCA = rCA,
                    etfa = etfa,
                    muestreado_por_algoritmo = muestreado_por_algoritmo,
                    creator_user = creator_user
                    ).save()

            else:
                models.Servicio(
                    codigo_muestra = codigo_muestra, 
                    proyecto_id = proyecto, 
                    punto_de_muestreo = punto_de_muestreo.nombre,
                    tipo_de_muestra = tipo_de_muestra,
                    fecha_de_muestreo = fecha_de_muestreo,
                    envases = envases,
                    fecha_de_recepción = fecha_de_recepcion,
                    norma_de_referencia = norma_de_referencia,
                    rCA = rCA,
                    etfa = etfa,
                    muestreado_por_algoritmo = muestreado_por_algoritmo,
                    creator_user = creator_user
                    ).save()
                    

        for pid in parameters:
            models.ParametroDeMuestra(servicio_id = codigo_muestra, parametro_id= pid).save()

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
def service(request, service_id):
    service = models.Servicio.objects.get(pk=service_id)
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    parameters = models.ParametroDeMuestra.objects.filter(servicio_id=service_id)
    rca = models.RCACliente.objects.get(pk=service.rCA)
    norma = models.NormaDeReferencia.objects.get(pk=service.norma_de_referencia)
    return render(request, 'lims/service.html', {
        'service': service,
        'parametros': parametros,
        'parameters': parameters,
        'rca': rca,
        'norma': norma,
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
    service_parameters = models.ParametroDeMuestra.objects.all().order_by('servicio_id')
    parametros = models.ParametroEspecifico.objects.all()
    parameters = parametros
    if request.method == 'POST':
        print(request.POST)
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                })
            else:
                service_parameters = models.ParametroDeMuestra.objects.filter(parametro_id=request.POST['parametro']).order_by('servicio_id')
                return render(request, 'lims/service_parameters.html',{
                    'service_parameters': service_parameters,
                    'parametros': parametros,
                    'parameters': parameters,
                    })
        else:
            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
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

