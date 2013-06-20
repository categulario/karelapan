from django.contrib import admin
from apps.sitio.models import *

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'autor', 'fecha', 'pegajoso')
    ordering = ('fecha',)
    list_filter  = ('fecha', 'pegajoso')

class AvisoAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'tipo', 'mostrado')
    ordering = ('tipo',)
    list_filter = ('tipo', 'mostrado')

class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'respuesta_full', 'ordenacion', 'mostrado')
    ordering = ('ordenacion',)

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Aviso, AvisoAdmin)
admin.site.register(PreguntaFrecuente, PreguntaFrecuenteAdmin)
