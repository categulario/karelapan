from apps.evaluador.models import Problema
from django.shortcuts import get_object_or_404
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return HttpResponse("Bienvenido a la API de Karelapan. Ejecute un comando.", content_type="text/plain")

def mundo_ejemplo(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo, content_type='text/plain')

def mundo_ejemplo_solucion(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo_resuelto, content_type='text/plain')
