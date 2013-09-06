# -*- coding:utf-8 -*-
from django import forms
from apps.usuarios.models import Perfil, Grupo, Usuario
from django.core.exceptions import ValidationError
import re

def valida_nombre_de_usuario(cadena):
    caracteres = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890@.-_+'
    for i in cadena:
        if i not in caracteres:
            raise ValidationError('Caracter no válido')
    try:
        u = Usuario.objects.get(username=cadena)
        raise ValidationError('Este nombre de usuario ya está en uso')
    except Usuario.DoesNotExist:
        pass

def valida_correo(cadena):
    try:
        u = Usuario.objects.get(email=cadena)
        raise ValidationError('Este correo electrónico ya está en uso')
    except Usuario.DoesNotExist:
        pass
    m = re.match('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}', cadena)
    if m:
        a, b = m.span()
        if b != len(cadena):
            raise ValidationError('No es un correo válido')
    else:
        raise ValidationError('No es un correo válido')

class PerfilForm(forms.ModelForm):
    required_css_class = 'required'
    nombre_asesor       = forms.CharField(required=False)
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Perfil
        exclude = ('usuario', 'grupos', 'problemas_resueltos', 'puntaje', 'sexo', 'fecha_nacimiento', 'ultima_omi', 'inscripciones', 'nombre_completo', 'asesor')

class RegistroForm(forms.ModelForm):
    correo              = forms.EmailField(validators=[valida_correo])
    nombre_asesor       = forms.CharField(required=False)
    nombre_de_usuario   = forms.CharField(validators=[valida_nombre_de_usuario])
    contrasenia         = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    repetir_contrasenia = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    required_css_class = 'required'
    class Meta:
        model = Perfil
        exclude = ('usuario', 'problemas_resueltos', 'puntaje', 'grupos', 'nombre_completo', 'asesor', 'inscripciones', 'confirm_token')
