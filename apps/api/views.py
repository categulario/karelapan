# -*- coding:utf-8 -*-
from apps.evaluador.models import Problema, Envio, Concurso, Consulta
from apps.usuarios.models import Usuario
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
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
        usuarios = Usuario.objects.filter(nombre_escuela__icontains=request.GET['q']).order_by('nombre_escuela').distinct('nombre_escuela')
        escuelas = [str(usuario.nombre_escuela) for usuario in usuarios]
        return HttpResponse(json.dumps(escuelas), content_type='text/plain')
    else:
        return HttpResponse('[]', content_type='text/plain')

def descarga_codigo(request, id_envio):
    envio = get_object_or_404(Envio, pk=id_envio)
    if envio.usuario == request.user and request.user.concursos_activos().count() == 0:
        return HttpResponse(envio.codigo, content_type='text/plain')
    else:
        return HttpResponse('Forbidden', content_type='text/plain')

def envio(request, id_envio, id_concurso=None):
    envio = get_object_or_404(Envio, pk=id_envio)
    if id_concurso:
        concurso = get_object_or_404(Concurso, pk=id_concurso)
    else:
        concurso = None
    if envio.usuario == request.user and envio.concurso == concurso:
        if not concurso and request.user.concursos_activos().count() > 0:
            return HttpResponse('Forbidden', content_type='text/plain')
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

@csrf_exempt
def hacer_consulta(request):
    """Recibe una consulta de un usuario durante el examen"""
    id_concurso = request.POST.get('concurso')
    concurso    = get_object_or_404(Concurso, pk=id_concurso)
    id_problema = request.POST.get('problema')
    problema    = get_object_or_404(Problema, pk=id_problema)
    mensaje     = request.POST.get('mensaje')
    if concurso in request.user.concursos_activos() and problema in concurso.problemas.all():
        if mensaje != '':
            if request.user.puede_hacer_consulta(concurso):
                consulta = Consulta(concurso=concurso, problema=problema, usuario=request.user, mensaje=request.POST.get('mensaje'), ip=request.META['REMOTE_ADDR'])
                consulta.save()
                return HttpResponse('ok', content_type='text/plain')
            else:
                return HttpResponse('Ha terminado el periodo de consultas', content_type='text/plain')
        else:
            return HttpResponse('El mensaje está vacío', content_type='text/plain')
    else:
        return HttpResponse('Ya no tienes permiso de hacer preguntas', content_type='text/plain')
