"""LIMS models."""

from django.db import models

# Create your models here.
class Manufacturer(models.Model):
    """Manufacture model."""

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name