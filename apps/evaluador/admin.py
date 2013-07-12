from django.contrib import admin
from apps.evaluador.models import *

def ocultar_problema(modeladmin, request, queryset):
    queryset.update(publico=False)
ocultar_problema.short_description = "Oculta los problemas seleccionados"

def mostrar_problema(modeladmin, request, queryset):
    queryset.update(publico=True)
mostrar_problema.short_description = "Muestra los problemas seleccionados"

def activar_concurso(modeladmin, request, queryset):
    queryset.update(activo=True)
activar_concurso.short_description = "Activa los concursos seleccionados"

def desactivar_concurso(modeladmin, request, queryset):
    queryset.update(activo=False)
desactivar_concurso.short_description = "Desactiva los concursos seleccionados"

class ConsideracionInline(admin.StackedInline):
    model = Consideracion
    extra = 1

class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'nivel')
    ordering = ('nivel',)

class ProblemaAdmin(admin.ModelAdmin):
    list_display        = ('nombre', 'veces_resuelto', 'veces_intentado', 'nivel', 'autor', 'publico')
    list_filter         = ('nivel', 'publico')
    inlines             = [ConsideracionInline]
    actions             = [ocultar_problema, mostrar_problema]
    prepopulated_fields = {"nombre_administrativo": ("nombre",)}
    readonly_fields     = ('veces_resuelto', 'veces_intentado', 'mejor_tiempo', 'mejor_puntaje')

class ConcursoAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'lista_grupos', 'activo', 'ranking_publico')
    list_filter     = ('fecha_inicio',)
    actions         = [activar_concurso, desactivar_concurso]

class ParticipacionAdmin(admin.ModelAdmin):
    list_display    = ('id', 'usuario', 'concurso', 'puntaje')
    list_filter     = ('concurso', 'puntaje')
    readonly_fields = ('puntaje',)

class EnvioAdmin(admin.ModelAdmin):
    list_display    = ('id', 'usuario', 'problema', 'hora', 'estatus', 'puntaje', 'tiempo_ejecucion', 'resultado', 'concurso', 'ip')
    list_filter     = ('problema', 'hora', 'estatus', 'puntaje', 'resultado', 'concurso')
    readonly_fields = ('usuario', 'problema', 'puntaje', 'codigo', 'codigo_archivo', 'tiempo_ejecucion', 'resultado', 'mensaje', 'concurso', 'ip', 'casos')

class ConsultaAdmin(admin.ModelAdmin):
    list_display    = ('mensaje', 'hora', 'concurso', 'problema', 'usuario', 'respuesta', 'leido', 'descartado')
    list_filter     = ('concurso', 'problema', 'leido')
    readonly_fields = ('concurso', 'problema', 'usuario', 'hora', 'ip')
    ordering        = ('concurso', 'problema', '-hora')

admin.site.register(Nivel, NivelAdmin)
admin.site.register(Problema, ProblemaAdmin)
admin.site.register(Concurso, ConcursoAdmin)
admin.site.register(Participacion, ParticipacionAdmin)
admin.site.register(Envio, EnvioAdmin)
admin.site.register(Consulta, ConsultaAdmin)
