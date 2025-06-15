from django import forms
from .models import Persona

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username / Email',
                                                             'class': 'login__input'}))

    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                             'class': 'login__input'}))

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'numero_casa', 'tipo', 'vehiculo', 'patente','foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
        }    