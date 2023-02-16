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

        model = models.ParametroEspecifico

        fields = '__all__'


class ServiceForm(forms.ModelForm):
    
    class Meta:

        model = models.Servicio

        fields = '__all__'

class ParameterMuestraForm(forms.ModelForm):

    class Meta:

        model = models.ParametroDeMuestra

        fields = '__all__'