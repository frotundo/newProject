from django.contrib import admin
from . import models

# Register your models here.

class RCAClient(admin.StackedInline):
    model = models.RCACliente
    extra = 0

class RepresentanteLegalClient(admin.StackedInline):
    model = models.RepresentanteLegalCliente
    extra = 0

class ContactClient(admin.StackedInline):
    model = models.ContactoCliente
    extra = 0

class SamplePointClient(admin.StackedInline):
    model = models.PuntoDeMuestreo
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    inlines = [RepresentanteLegalClient, ContactClient, SamplePointClient, RCAClient]


admin.site.register(models.Cliente, ClientAdmin)
admin.site.register(models.Proyecto)
admin.site.register(models.NormaDeReferencia)
admin.site.register(models.Servicio)
admin.site.register(models.TipoDeMuestra)