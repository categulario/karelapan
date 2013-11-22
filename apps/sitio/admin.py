from django.contrib import admin
from apps.sitio.models import *
from apps.usuarios.models import Usuario

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'autor', 'fecha', 'pegajoso')
    ordering = ('-fecha',)
    list_filter  = ('fecha', 'pegajoso')
    readonly_fields = ('autor',)

    def save_model(self, request, obj, form, change):
        obj.autor = Usuario.objects.get(pk=request.user.id)
        obj.save()

class AvisoAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'tipo', 'mostrado', 'caducidad', 'activo')
    ordering = ('tipo',)
    list_filter = ('tipo', 'mostrado')

class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'respuesta_full', 'ordenacion', 'mostrado')
    ordering = ('ordenacion',)

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Aviso, AvisoAdmin)
admin.site.register(PreguntaFrecuente, PreguntaFrecuenteAdmin)
