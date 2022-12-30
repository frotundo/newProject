from django import forms

from . import models

# class AddProjectForm(forms.ModelForm):

#     class Meta:

#         model = models.Proyecto

#         fields = {
#             'nombre',
#             'codigo',
#             'tipo_de_muestra'
            
#         }

#         label = {
#             'nombre':'Nombre',
#             'creator_user': 'Creado por'
#         }

#         widgets = {
#             'nombre': forms.TextInput(),
#             'creator_user': forms.TextInput(),
#         }

class ProjectForm(forms.ModelForm):

    class Meta:

        model = models.Proyecto

        fields = '__all__'

