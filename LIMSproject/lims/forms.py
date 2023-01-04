from django import forms

from . import models

class ProjectForm(forms.ModelForm):

    class Meta:

        model = models.Proyecto

        fields = '__all__'

class ServiceForm(forms.ModelForm):

    class Meta:

        model = models.Servicio

        fields = '__all__'

class ParameterForm(forms.ModelForm):

    class Meta:

        model = models.Parametro

        fields = '__all__'

class ETFAForm(forms.ModelForm):

    class Meta:

        model = models.ETFA

        fields = '__all__'
