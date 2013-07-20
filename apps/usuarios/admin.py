from django.contrib import admin
from django.contrib import auth
from apps.usuarios.models import *
from django.utils.translation import ugettext, ugettext_lazy as _

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'correo', 'estado', 'subsistema', 'asesor', 'problemas_resueltos', 'puntaje', 'ultima_omi', 'lista_grupos')
    list_filter = ('subsistema', 'problemas_resueltos', 'puntaje', 'estado')
    ordering = ['nombre']
    search_fields = ('correo', 'nombre', 'appat', 'apmat')

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'elegible')


admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Olimpiada)
