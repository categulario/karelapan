from django.contrib import admin
from django.contrib import auth
from apps.usuarios.models import *
from django.utils.translation import ugettext, ugettext_lazy as _

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'estado', 'subsistema', 'asesor', 'problemas_resueltos', 'puntaje', 'ultima_omi', 'lista_grupos')
    list_filter = ('subsistema', 'problemas_resueltos', 'puntaje', 'estado')
    ordering = ['nombre']
    search_fields = ('correo', 'nombre', 'appat', 'apmat')
    filter_horizontal = ('groups', 'user_permissions',)
    exclude = ('password',)

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'elegible')


admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Olimpiada)
