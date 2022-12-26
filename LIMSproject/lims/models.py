"""LIMS models."""

from django.db import models



class Cliente(models.Model):
    """Analysis model."""

    titular = models.CharField(max_length=200, unique=True)
    direccion = models.CharField(max_length=200)
    rut = models.CharField(max_length=10, unique=True)
    actividad = models.CharField(max_length=250)
    #email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.titular

class ContactoCliente(models.Model):
    """Contact client model."""
    
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre


class PuntoDeMuestreo(models.Model):
    """Sample point model."""
    
    nombre = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class NormaDeReferencia(models.Model):
    """Reference standard model."""
    
    norma = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.norma


class RCACliente(models.Model):
    """Legal representative model."""

    rca_asociada = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.rca_asociada



class Proyecto(models.Model):
    """Project model."""
    
    nombre_de_Proyecto = models.CharField(max_length=254)
    codigo_de_proyecto = models.CharField(max_length=10)
    tipo_de_Muestreo = models
    norma_de_referencia = models
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    punto_de_muestreo = models.ForeignKey(PuntoDeMuestreo, null=True, blank=True, on_delete=models.PROTECT)
    norma_de_referencia = models.ForeignKey(NormaDeReferencia, null=True, blank=True, on_delete=models.PROTECT)
    rCA = models.ForeignKey(RCACliente, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre_de_Proyecto


class Servicio(models.Model):
    """Service model."""

    codigo_muestra = models.CharField(max_length=50, unique=True)
    fecha_de_muestreo = models.DateField()
    fecha_de_recepción = models.DateField()
    norma_de_referencia = models.ManyToManyField(NormaDeReferencia)
    rCA = models.ManyToManyField(RCACliente)
    #punto_de_muestreo =  #Revisar


class Envase(models.Model):
    """ Envase model."""

    nombre = models.CharField(max_length=100)
    volumen = models.CharField(max_length=10)
    material = models.CharField(max_length=100)
    Preservante = models.CharField(max_length=254)
    servicio = models.ManyToManyField(Servicio) #Revisar

    def __str__(self):
        return self.nombre


class Parametro(models.Model):
    pass

class RepresentanteLegalCliente(models.Model):
    """Legal representative model."""

    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=200, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre



class Metodo(models.Model):
    """Method model."""
    nombre = models.TextField()




