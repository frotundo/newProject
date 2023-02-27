"""LIMS models."""

from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    """Analysis model."""

    titular = models.CharField(max_length=200, unique=True)
    direccion = models.CharField(max_length=200)
    rut = models.CharField(max_length=10, unique=True)
    actividad = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.titular


class ContactoCliente(models.Model):
    """Contact client model."""
    
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PuntoDeMuestreo(models.Model):
    """Sample point model."""
    
    nombre = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class LugarDeMonitoreo(models.Model):
    """Monitoring place model."""
    
    nombre = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class NormaDeReferencia(models.Model):
    """Reference standard model."""
    
    norma = models.CharField(max_length=254, unique=True)
    descripcion =models.CharField(max_length=254, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.norma


class RCACliente(models.Model):
    """Legal representative model."""

    rca_asociada = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.rca_asociada


class Envase(models.Model):
    """ Envase model."""

    codigo = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=100)
    volumen = models.CharField(max_length=10)
    material = models.CharField(max_length=100)
    preservante = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo

class Filtro(models.Model):
    """ Envase model."""

    codigo = models.CharField(primary_key=True, max_length=15)
    descripcion = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Metodo(models.Model):
    """Method model."""
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class TipoDeMuestra(models.Model):
    """Sample type model."""
    nombre = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

        
class ParametroEspecifico(models.Model):
    '''Specific parameter model.'''

    ensayo = models.CharField(max_length=254)
    codigo = models.CharField(max_length=254, unique=True)
    metodo = models.CharField(max_length=254)
    LDM = models.CharField(max_length=10, null=True, blank=True)
    LCM = models.CharField(max_length=10, null=True, blank=True)
    unidad = models.CharField(max_length=20, null=True, blank=True)
    tipo_de_muestra = models.CharField(max_length=100)
    codigo_etfa = models.CharField(max_length=20, null=True, blank=True)
    acreditado = models.CharField(max_length=20, null=True, blank=True)
    envase = models.ForeignKey(Envase, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)


    def __str__(self):
        return self.ensayo


class RepresentanteLegalCliente(models.Model):
    """Legal representative model."""

    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    """Project model."""
    
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=254)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    parametros_cotizados = models.ManyToManyField(ParametroEspecifico)
    parametros_externos = models.ManyToManyField(ParametroEspecifico, related_name='parametros_analisis_externos')
    cotizado = models.BooleanField(null=True, blank=True,) 
    tipo_de_muestra = models.CharField(max_length=100, null=True, blank=True)
    etfa = models.BooleanField(null=True, blank=True,) 
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ModeloDeServicioDeFiltro(models.Model):
    """Service model."""

    codigo_modelo = models.CharField(max_length=200, unique=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    parametros = models.ManyToManyField(ParametroEspecifico)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    area = models.CharField(max_length=200, null=True, blank=True,)
    punto_de_muestreo = models.CharField(max_length=200)
    tipo_de_muestra = models.CharField(max_length=200)
    observacion = models.TextField(null=True, blank=True,)
    filtro = models.ForeignKey(Filtro, on_delete=models.PROTECT)
    norma_de_referencia = models.ForeignKey(NormaDeReferencia, on_delete=models.PROTECT)
    responsable = models.CharField(max_length=200)
    rCA = models.ForeignKey(RCACliente, on_delete=models.PROTECT)
    etfa = models.BooleanField() 
    muestreado_por_algoritmo = models.CharField(max_length=254)
    created = models.DateTimeField()
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo_muestra
    

class Servicio(models.Model):
    """Service model."""

    codigo = models.CharField(max_length=50, primary_key=True, unique=True)
    codigo_muestra = models.CharField(max_length=50, unique=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    cliente = models.CharField(max_length=5)
    area = models.CharField(max_length=200, null=True, blank=True,)
    punto_de_muestreo = models.CharField(max_length=200)
    tipo_de_muestra = models.CharField(max_length=200)
    fecha_de_muestreo = models.DateField(null=True, blank=True,)
    envases = models.TextField(null=True, blank=True,)
    filtros = models.ForeignKey(Filtro, on_delete=models.PROTECT,null=True, blank=True)
    observacion = models.TextField(null=True, blank=True,)
    fecha_de_recepcion = models.DateField(null=True, blank=True,)
    fecha_de_entrega_cliente = models.DateField(null=True, blank=True,)
    fecha_de_contenedores_o_filtros = models.DateField(null=True, blank=True,)
    norma_de_referencia = models.CharField(max_length=254)
    responsable = models.CharField(max_length=200)
    rCA = models.CharField(max_length=254)
    etfa = models.BooleanField(default=False) 
    modelo = models.ForeignKey(ModeloDeServicioDeFiltro, on_delete=models.PROTECT, null=True, blank=True)
    muestreado_por_algoritmo = models.CharField(max_length=254)
    created = models.DateTimeField()
    creator_user = models.CharField(max_length=100)
    editor_sample_code = models.CharField(max_length=100, null=True, blank=True,)

    def __str__(self):
        return self.codigo_muestra
    

class Batch(models.Model):
    "Batch model."
    codigo = models.CharField(max_length=10, primary_key=True)
    parametro = models.CharField(max_length=50, null=True, blank=True)
    responsable_asignado = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    responsable = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    creator_user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.codigo


class ParametroDeMuestra(models.Model):
    """Sample paramenter model."""

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, null=True, blank=True)
    codigo_servicio = models.CharField(max_length=100)
    parametro = models.ForeignKey(ParametroEspecifico, on_delete=models.CASCADE)
    analisis_externos = models.BooleanField(default=False)
    responsable_de_analisis = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    fecha_de_inicio = models.DateTimeField(null=True, blank=True,)
    fecha_de_terminado = models.DateTimeField(null=True, blank=True,)
    resultado = models.FloatField(null=True, blank=True,)
    factor_de_dilucion = models.IntegerField(null=True, blank=True,)
    resultado_final = models.FloatField(null=True, blank=True,)
    peso_inicial = models.FloatField(null=True, blank=True,)
    peso_final = models.FloatField(null=True, blank=True,)
    ensayo = models.CharField(max_length=50, null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.codigo_servicio

    
class ParametroDeMuestraDescartada(models.Model):
    """Sample paramenter model dropped."""

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, null=True, blank=True)
    codigo_servicio = models.CharField(max_length=100)
    parametro = models.ForeignKey(ParametroEspecifico, on_delete=models.CASCADE)
    responsable_de_analisis = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    fecha_de_inicio = models.DateTimeField(null=True, blank=True,)
    fecha_de_terminado = models.DateTimeField(null=True, blank=True,)
    resultado = models.FloatField(null=True, blank=True,)
    factor_de_dilucion = models.IntegerField(null=True, blank=True,)
    resultado_final = models.FloatField(null=True, blank=True,)
    peso_inicial = models.FloatField(null=True, blank=True,)
    peso_final = models.FloatField(null=True, blank=True,)
    ensayo = models.CharField(max_length=50, null=True, blank=True,)
    created = models.DateTimeField()
    discarder = models.CharField(max_length=50, null=True, blank= True)
    discarded = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.codigo_servicio
