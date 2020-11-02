from django import forms
from django.contrib.admin import widgets
from dateutil.parser import parse
from django.core import validators
from django.core.exceptions import ValidationError
import datetime


class FormInicio(forms.Form):
    personas = forms.ChoiceField(initial='',choices=((1,"1 Persona"),(2,"2 Personas"),(3,"3 Personas"),(4,"4 Personas")), required=True, label="Huéspedes")
    fechainicio = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Desde")
    fechafin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Hasta" )

    def clean(self):
        finicio = self.cleaned_data['fechainicio']
        ffin = self.cleaned_data['fechafin']
        if finicio > ffin:
            raise ValidationError("La fecha de entrada no puede ser mayor que la de salida")
            
        if finicio < datetime.date.today():
            raise ValidationError("La fecha de entrada no puede ser menor a la de hoy")
            
        if ffin > datetime.date(2020, 12 , 31):
            raise ValidationError("Solo se permiten reservas hasta el día 31-12-2020")
        

class FormReserva(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.IntegerField(required = True)

class FormLoginUser(forms.Form):
    localizador = forms.CharField(min_length=6,max_length=6, required=True)
    email = forms.EmailField(required=True)
