from django.contrib import admin
from apps.libro.models import *

class CodigoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'usado', 'fecha_activacion', 'usuario', 'libro')
    list_filter = ('usado', 'libro')

class CapituloInline(admin.StackedInline):
    model = Capitulo
    extra = 1

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'grupo', 'costo')
    prepopulated_fields = {"grupo": ("titulo",)}
    inlines = [CapituloInline]

admin.site.register(Codigo, CodigoAdmin)
admin.site.register(Libro, LibroAdmin)
