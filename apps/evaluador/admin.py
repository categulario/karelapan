from django.contrib import admin
from apps.evaluador.models import *

class ConsideracionInline(admin.StackedInline):
    model = Consideracion
    extra = 1

class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'nivel')
    ordering = ('nivel',)

class ProblemaAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'veces_resuelto', 'veces_intentado', 'nivel', 'autor', 'publico')
    list_filter     = ('nivel', 'publico')
    inlines         = [ConsideracionInline]

class ConcursoAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'autor', 'activo')
    list_filter     = ('fecha_inicio',)

class ParticipacionAdmin(admin.ModelAdmin):
    list_display    = ('id', 'usuario', 'concurso', 'puntaje')
    list_filter     = ('concurso', 'puntaje')

admin.site.register(Nivel, NivelAdmin)
admin.site.register(Problema, ProblemaAdmin)
admin.site.register(Concurso, ConcursoAdmin)
admin.site.register(Participacion, ParticipacionAdmin)
