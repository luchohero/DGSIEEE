from django import forms
from django.template import RequestContext
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
	


class DatosForm(forms.ModelForm):
	class Meta:
		model = Datos

class EstadoForm(forms.ModelForm):
	class Meta:
		model = Estado
