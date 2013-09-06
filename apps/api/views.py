# -*- coding:utf-8 -*-
from apps.evaluador.models import Problema, Envio, Concurso, Consulta, Participacion
from apps.usuarios.models import Usuario
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.db.models import Q
import json
import csv

def index(request):
    return HttpResponse("Hola, humano", content_type="text/plain")

def mundo_ejemplo(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo, content_type='text/plain')

def mundo_ejemplo_solucion(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    return HttpResponse(problema.mundo_resuelto, content_type='text/plain')

@login_required
def mundo_ejemplo_concurso(request, id_concurso, id_problema):
    concurso    = get_object_or_404(Concurso, pk=id_concurso)
    problema    = get_object_or_404(Problema, pk=id_problema)
    usuario = Usuario.objects.get(pk=request.user.id)
    if concurso in usuario.concursos_activos(solo_importantes=False) and problema in concurso.problemas.all():
        problema = get_object_or_404(Problema, pk=id_problema)
        return HttpResponse(problema.mundo, content_type='text/plain')
    else:
        return HttpResponse('{}', content_type='text/plain')

@login_required
def mundo_ejemplo_solucion_concurso(request, id_concurso, id_problema):
    concurso    = get_object_or_404(Concurso, pk=id_concurso)
    problema    = get_object_or_404(Problema, pk=id_problema)
    usuario = Usuario.objects.get(pk=request.user.id)
    if concurso in usuario.concursos_activos(solo_importantes=False) and problema in concurso.problemas.all():
        problema = get_object_or_404(Problema, pk=id_problema)
        return HttpResponse(problema.mundo_resuelto, content_type='text/plain')
    else:
        return HttpResponse('{}', content_type='text/plain')

def nombres_escuela(request):
    if 'q' in request.GET:
        usuarios = Usuario.objects.filter(perfil__nombre_escuela__icontains=request.GET['q']).order_by('perfil__nombre_escuela').distinct('perfil__nombre_escuela')
        escuelas = [str(usuario.perfil.nombre_escuela.encode('utf-8')) for usuario in usuarios]
        return HttpResponse(json.dumps(escuelas), content_type='text/plain')
    else:
        return HttpResponse('[]', content_type='text/plain')

def nombres_asesores(request):
    if 'q' in request.GET:
        usuarios = Usuario.objects.filter(perfil__nombre_completo__icontains=request.GET['q'])
        nombres = [{'nombre': str(usuario.get_full_name().encode('utf-8')), 'id':usuario.id} for usuario in usuarios]
        return HttpResponse(json.dumps(nombres), content_type='text/plain')
    else:
        return HttpResponse('[]', content_type='text/plain')

@login_required
def obten_nombre_asesor(request, id_asesor):
    asesor = get_object_or_404(Usuario, pk=id_asesor)
    return HttpResponse(asesor.perfil.nombre_completo, content_type='text/plain')

def existe_usuario(request, nombre_usuario):
    try:
        Usuario.objects.get(username=nombre_usuario)
        return HttpResponse('sip', content_type='text/plain')
    except Usuario.DoesNotExist:
        return HttpResponse('nope', content_type='text/plain')

@login_required
def descarga_codigo(request, id_envio):
    """Le ofrece a un usuario la posibilidad de descargar uno de sus
    códigos enviados"""
    envio = get_object_or_404(Envio, pk=id_envio)
    usuario = Usuario.objects.get(pk=request.user.id)
    if envio.usuario.id == usuario.id and usuario.concursos_activos().count() == 0:
        response = HttpResponse(envio.codigo, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s.karel"'%(envio.problema.nombre_administrativo, envio.id)
        return response
    else:
        return HttpResponse('Forbidden', content_type='text/plain')

def descarga_mundo(request, id_problema):
    problema = get_object_or_404(Problema, pk=id_problema, publico=True)
    response = HttpResponse(problema.mundo, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.world"'%(problema.nombre_administrativo)
    return response

@login_required
def envio(request, id_envio, id_concurso=None):
    """Ofrece el veredicto de un envío a un usuario"""
    envio = get_object_or_404(Envio, pk=id_envio)
    if id_concurso:
        concurso = get_object_or_404(Concurso, pk=id_concurso)
    else:
        concurso = None
    if envio.usuario == request.user and envio.concurso == concurso:
        usuario = Usuario.objects.get(pk=request.user.id)
        if not concurso and usuario.participa_en_concurso(solo_importantes=False):#No se cargan veredictos durante el concurso
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
@login_required
def hacer_consulta(request):
    """Recibe una consulta de un usuario durante el examen"""
    id_concurso = request.POST.get('concurso')
    concurso    = get_object_or_404(Concurso, pk=id_concurso)
    id_problema = request.POST.get('problema')
    problema    = get_object_or_404(Problema, pk=id_problema)
    mensaje     = request.POST.get('mensaje')
    usuario = Usuario.objects.get(pk=request.user.id)
    if concurso in usuario.concursos_activos(solo_importantes=False) and problema in concurso.problemas.all():
        if mensaje != '':
            if usuario.puede_hacer_consulta(concurso):
                if Consulta.objects.filter(concurso=concurso, problema=problema, usuario=usuario, leido=False).count() == 0:
                    consulta = Consulta(concurso=concurso, problema=problema, usuario=usuario, mensaje=request.POST.get('mensaje'), ip=request.META['REMOTE_ADDR'])
                    consulta.save()
                    return HttpResponse('ok', content_type='text/plain')
                else:
                    return HttpResponse('No puedes hacer una pregunta teniendo otras pendientes para el mismo problema', content_type='text/plain')
            else:
                return HttpResponse('Ha terminado el periodo de consultas', content_type='text/plain')
        else:
            return HttpResponse('El mensaje está vacío', content_type='text/plain')
    else:
        return HttpResponse('Ya no tienes permiso de hacer preguntas', content_type='text/plain')

@csrf_exempt
@permission_required('evaluador.puede_ver_ranking')
def responde_consulta(request):
    """Recibe la respuesta a una consulta y la procesa"""
    id_consulta = request.POST.get('consulta')
    respuesta = request.POST.get('respuesta')
    if request.POST.get('rechazar'):
        consulta = get_object_or_404(Consulta, pk=id_consulta)
        consulta.descartado = True
        consulta.leido = True
        consulta.save()
        return HttpResponse('consulta rechazada', content_type='text/plain')
    if respuesta == '':
        return HttpResponse('Se te olvidó escribir la respuesta', content_type='text/plain')
    consulta = get_object_or_404(Consulta, pk=id_consulta)
    consulta.leido = True
    consulta.respuesta = respuesta
    consulta.save()
    return HttpResponse('ok', content_type='text/plain')

@permission_required('evaluador.puede_ver_ranking')
def busca_consultas(request, id_concurso):
    """Busca consultas sin revisar"""
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    consultas = Consulta.objects.filter(concurso=concurso, leido=False)
    consultas_list = []
    for consulta in consultas:
        consultas_list.append({
            'id': consulta.id,
            'mensaje': consulta.mensaje,
            'usuario': unicode(consulta.usuario),
            'problema': unicode(consulta.problema),
            'hora': unicode(consulta.hora)
        })
    return HttpResponse(json.dumps(consultas_list), content_type='text/plain')

@login_required
def consultas(request, id_concurso, id_problema):
    """Le da a un usuario sus consultas"""
    concurso    = get_object_or_404(Concurso, pk=id_concurso)
    problema    = get_object_or_404(Problema, pk=id_problema)
    usuario = Usuario.objects.get(pk=request.user.id)
    if concurso in usuario.concursos_activos(solo_importantes=False) and problema in concurso.problemas.all():
        consultas = Consulta.objects.filter(problema=problema, concurso=concurso, usuario=usuario, leido=True)
        consulta_list = []
        for consulta in consultas:
            consulta_list.append({
                'mensaje': consulta.mensaje,
                'respuesta': consulta.respuesta,
                'descartado': consulta.descartado,
                'id': consulta.id
            })
        consultas = Consulta.objects.filter(problema=problema, concurso=concurso, usuario=None, leido=True) #Las aclaraciones
        for consulta in consultas:
            consulta_list.append({
                'mensaje': consulta.mensaje,
                'respuesta': consulta.respuesta,
                'descartado': consulta.descartado,
                'id': consulta.id
            })
        return HttpResponse(json.dumps(consulta_list), content_type='text/plain')
    else:
        return HttpResponse(json.dumps([]), content_type='text/plain')

@permission_required('evaluador.puede_ver_ranking')
def ranking_csv(request, id_concurso):
    """Genera el PDF a partir del ranking de un concurso"""
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ranking_%s.csv"'%concurso.nombre

    writer = csv.writer(response)
    writer.writerow(['Lugar', 'Usuario', 'Escuela', 'Subsistema', 'Puntos'] + [problema.nombre.encode('utf-8') for problema in concurso.problemas.all()])

    i = 1
    for participacion in Participacion.objects.filter(concurso=concurso).order_by('-puntaje'):
        writer.writerow([
            i,
            participacion.usuario.perfil.nombre_completo.encode('utf-8'),
            participacion.usuario.perfil.nombre_escuela.encode('utf-8'),
            participacion.usuario.perfil.subsistema.encode('utf-8'),
            participacion.puntaje
        ] + [Usuario(participacion.usuario).mejor_puntaje(problema, concurso) for problema in concurso.problemas.all()])
        i += 1

    return response

@csrf_exempt
@permission_required('evaluador.puede_ver_ranking')
def aclaracion(request, id_concurso):
    """Permite hacer una aclaración general"""
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    id_problema = request.POST.get('problema')
    problema = get_object_or_404(Problema, pk=id_problema)
    if request.POST.get('respuesta') != '':
        consulta = Consulta(concurso=concurso, problema=problema, mensaje='[Aclaración]', respuesta=request.POST.get('respuesta'), leido=True, ip='127.0.0.1')
        consulta.save()
        return HttpResponse('ok', content_type='text/plain')
    else:
        return HttpResponse('Hay campos importantes vacíos', content_type='text/plain')
