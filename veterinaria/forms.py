from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'nacimiento', 'celular', 'direccion', 'rut', 'password']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tus nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tus apellidos'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo'}),
            'nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'nacimiento'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu celular'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu direccion'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}),
        }
