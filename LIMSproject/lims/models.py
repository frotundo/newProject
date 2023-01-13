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


class NormaDeReferencia(models.Model):
    """Reference standard model."""
    
    norma = models.CharField(max_length=254, unique=True)
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

    nombre = models.CharField(max_length=100)
    volumen = models.CharField(max_length=10)
    material = models.CharField(max_length=100)
    preservante = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Metodo(models.Model):
    """Method model."""
    nombre = models.CharField(max_length=254)
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
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Service model."""

    codigo_muestra = models.CharField(max_length=50, primary_key=True, unique=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    cliente = models.CharField(max_length=5)
    punto_de_muestreo = models.CharField(max_length=200)
    tipo_de_muestra = models.CharField(max_length=200)
    fecha_de_muestreo = models.DateField(null=True, blank=True,)
    envases = models.TextField(null=True, blank=True,)
    fecha_de_recepción = models.DateField(null=True, blank=True,)
    norma_de_referencia = models.CharField(max_length=254)
    responsable = models.CharField(max_length=200)
    rCA = models.CharField(max_length=254)
    etfa = models.BooleanField() 
    muestreado_por_algoritmo = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo_muestra


class ParametroDeMuestra(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    codigo_servicio = models.CharField(max_length=100)
    parametro = models.ForeignKey(ParametroEspecifico, on_delete=models.CASCADE)
    responsable_de_analisis = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    fecha_de_inicio = models.DateTimeField(null=True, blank=True,)
    fecha_de_terminado = models.DateTimeField(null=True, blank=True,)
    resultado = models.FloatField(null=True, blank=True,)
    factor_de_dilucion = models.IntegerField(null=True, blank=True,)
    resultado_final = models.FloatField(null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.codigo_muestra


class ETFA(models.Model):

    codigo = models.CharField(max_length=20, primary_key=True)
    parametro = models.ForeignKey(ParametroEspecifico, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.codigo
