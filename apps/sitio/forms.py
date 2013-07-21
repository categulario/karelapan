from django import forms
from apps.usuarios.models import Perfil, Grupo

class RegistroForm(forms.ModelForm):
    correo              = forms.EmailField()
    nombre_asesor       = forms.CharField(required=False)
    nombre_de_usuario   = forms.CharField()
    contrasenia         = forms.CharField(widget=forms.PasswordInput)
    repetir_contrasenia = forms.CharField(widget=forms.PasswordInput)
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    required_css_class = 'required'
    class Meta:
        model = Perfil
        exclude = ('usuario', 'problemas_resueltos', 'puntaje', 'grupos', 'nombre_completo', 'asesor', 'inscripciones')

class PerfilForm(forms.ModelForm):
    required_css_class = 'required'
    nombre_asesor       = forms.CharField(required=False)
    asesor              = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Perfil
        exclude = ('usuario', 'grupos', 'problemas_resueltos', 'puntaje', 'sexo', 'fecha_nacimiento', 'ultima_omi', 'inscripciones', 'nombre_completo', 'asesor')
