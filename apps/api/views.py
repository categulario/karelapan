from apps.evaluador.models import Problema, Envio
from apps.usuarios.models import Usuario
from django.shortcuts import get_object_or_404
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponse
import json

def index(request):
    return HttpResponse("Bienvenido a la API de Karelapan. Ejecute un comando.", content_type="text/plain")

def mundo_ejemplo(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo, content_type='text/plain')

def mundo_ejemplo_solucion(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo_resuelto, content_type='text/plain')

def nombres_escuela(request):
    if 'q' in request.GET:
        usuarios = Usuario.objects.filter(nombre_escuela__icontains=request.GET['q'])
        escuelas = ['"'+str(usuario.nombre_escuela)+'"' for usuario in usuarios]
        return HttpResponse('['+','.join(escuelas)+']', content_type='text/plain')
    else:
        return HttpResponse('[]', content_type='text/plain')

def descarga_codigo(request, id_envio):
    envio = get_object_or_404(Envio, pk=id_envio)
    if envio.usuario == request.user:
        return HttpResponse(envio.codigo, content_type='text/plain')
    else:
        return HttpResponse('Forbidden', content_type='text/plain')

def envio(request, id_envio):
    envio = get_object_or_404(Envio, pk=id_envio)
    if envio.usuario == request.user and envio.concurso == None:
        if envio.estatus == 'E':
            resultado = {
                'puntaje': envio.puntaje,
                'tiempo_ejecucion': envio.tiempo_ejecucion,
                'resultado': envio.resultado,
                'mensaje': envio.mensaje,
                'casos': json.loads(envio.casos)
            }
            return HttpResponse(json.dumps(resultado), content_type='text/plain')
        else:
            return HttpResponse(envio.estatus, content_type='text/plain')
    else:
        return HttpResponse('Forbidden', content_type='text/plain')
