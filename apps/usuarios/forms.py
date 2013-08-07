# -*- coding:utf-8 -*-
from django import forms
from apps.usuarios.models import Perfil, Grupo
from django.core.exceptions import ValidationError

def valida_nombre_de_usuario(cadena):
    caracteres = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890@.-_+'
    for i in cadena:
        if i not in caracteres:
            raise ValidationError('Caracter no válido')

class PerfilForm(forms.ModelForm):
    required_css_class = 'required'
    nombre_asesor       = forms.CharField(required=False)
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Perfil
        exclude = ('usuario', 'grupos', 'problemas_resueltos', 'puntaje', 'sexo', 'fecha_nacimiento', 'ultima_omi', 'inscripciones', 'nombre_completo', 'asesor')

class RegistroForm(forms.ModelForm):
    correo              = forms.EmailField()
    nombre_asesor       = forms.CharField(required=False)
    nombre_de_usuario   = forms.CharField(validators=[valida_nombre_de_usuario])
    contrasenia         = forms.CharField(widget=forms.PasswordInput, label="contraseña")
    repetir_contrasenia = forms.CharField(widget=forms.PasswordInput, label="repetir contraseña")
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    required_css_class = 'required'
    class Meta:
        model = Perfil
        exclude = ('usuario', 'problemas_resueltos', 'puntaje', 'grupos', 'nombre_completo', 'asesor', 'inscripciones')
