from django import forms
from apps.usuarios.models import Perfil, Grupo

class RegistroForm(forms.ModelForm):
    nombre_de_usuario   = forms.CharField()
    contrasenia         = forms.CharField(widget=forms.PasswordInput)
    repetir_contrasenia = forms.CharField(widget=forms.PasswordInput)
    nombre_asesor       = forms.CharField()
    asesor              = forms.CharField()
    required_css_class = 'required'
    class Meta:
        model = Perfil
        exclude = ('usuario', 'problemas_resueltos', 'puntaje', 'grupos')

class PerfilForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Perfil
        exclude = ('usuario', 'grupos', 'problemas_resueltos', 'puntaje', 'sexo', 'fecha_nacimiento', 'ultima_omi')
