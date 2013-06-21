from django import forms
from apps.usuarios.models import Usuario, Grupo

class RegistroForm(forms.ModelForm):
    grupo = forms.ModelMultipleChoiceField(queryset=Grupo.objects.filter(elegible=True))
    required_css_class = 'required'
    class Meta:
        model = Usuario
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'problemas_resueltos', 'puntaje', 'is_active', 'is_admin')
