from django.contrib import admin
from django.contrib import auth
from apps.usuarios.models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/exportar/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
export_selected_objects.short_description = "Exportar"

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'correo', 'estado', 'subsistema', 'asesor', 'problemas_resueltos', 'puntaje', 'ultima_omi', 'lista_grupos')
    list_filter = ('subsistema', 'problemas_resueltos', 'puntaje', 'estado')
    ordering = ['nombre']
    search_fields = ('nombre', 'appat', 'apmat')
    readonly_fields = ('problemas_resueltos', 'puntaje', 'usuario', 'confirm_token')

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'elegible')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login', 'date_joined', 'is_active')
    actions = ['activate_user', 'disable_user']
    def activate_user(modeladmin, request, queryset):
        queryset.update(is_active=True)
    activate_user.short_description = "Activa los usuarios seleccionados"
    def disable_user(modeladmin, request, queryset):
        queryset.update(is_active=False)
    disable_user.short_description = "Inhabilita a los usuarios seleccionados"

admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Olimpiada)
admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)

admin.site.add_action(export_selected_objects)
