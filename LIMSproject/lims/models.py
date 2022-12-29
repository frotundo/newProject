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
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PuntoDeMuestreo(models.Model):
    """Sample point model."""
    
    nombre = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
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
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
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


class Parametro(models.Model):
    '''Parameter model.'''

    ensayo = models.CharField(max_length=254, unique=True)
    metodo = models.ManyToManyField(Metodo)
    responsable = models.ForeignKey(User, on_delete=models.PROTECT)
    LDM = models.FloatField()
    LCM = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.ensayo


class Analysis(models.Model):
    '''Analysis model.'''
    pass
    # ensayo = 


class Servicio(models.Model):
    """Service model."""

    codigo_muestra = models.CharField(max_length=50, unique=True)
    fecha_de_muestreo = models.DateField()
    fecha_de_recepción = models.DateField()
    norma_de_referencia = models.ManyToManyField(NormaDeReferencia)
    rCA = models.ManyToManyField(RCACliente)
    envase = models.ManyToManyField(Envase) #Revisar
    #punto_de_muestreo =  #Revisar
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo_muestra


class RepresentanteLegalCliente(models.Model):
    """Legal representative model."""

    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
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


class Proyecto(models.Model):
    """Project model."""
    
    nombre = models.CharField(max_length=254)
    codigo = models.CharField(max_length=10)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    tipo_de_muestra = models.ForeignKey(TipoDeMuestra, null=True, blank=True, on_delete=models.PROTECT)
    punto_de_muestreo = models.ForeignKey(PuntoDeMuestreo, null=True, blank=True, on_delete=models.PROTECT)
    responsable_muestreo = models.CharField(max_length=254)
    norma_de_referencia = models.ForeignKey(NormaDeReferencia, null=True, blank=True, on_delete=models.PROTECT)
    rCA = models.ForeignKey(RCACliente, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    creator_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_de_Proyecto





