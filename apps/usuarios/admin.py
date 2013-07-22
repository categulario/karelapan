from django.contrib import admin
from django.contrib import auth
from apps.usuarios.models import *
from django.utils.translation import ugettext, ugettext_lazy as _

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'correo', 'estado', 'subsistema', 'asesor', 'problemas_resueltos', 'puntaje', 'ultima_omi', 'lista_grupos')
    list_filter = ('subsistema', 'problemas_resueltos', 'puntaje', 'estado')
    ordering = ['nombre']
    search_fields = ('correo', 'nombre', 'appat', 'apmat')
    readonly_fields = ('problemas_resueltos', 'puntaje', 'usuario')

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'elegible')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login', 'date_joined')

admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Olimpiada)
admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)
