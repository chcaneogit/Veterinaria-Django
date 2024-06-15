# forms.py

from django import forms

class LoginForm(forms.Form):
    rut = forms.CharField(label='RUT', max_length=8)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
