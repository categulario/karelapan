# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.sitio.models import Aviso, Noticia, PreguntaFrecuente
from apps.sitio.forms import RegistroForm, PerfilForm
from apps.evaluador.models import Nivel, Problema, Concurso, Envio, Participacion
from apps.usuarios.models import Usuario
from django.contrib import auth
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modules.recaptcha import verifica
from modules.badges import badgify
import datetime
import uuid

#~ data = {
    #~ 'GA'        : settings.GOOGLE_ANALYTHICS,
    #~ 'CA'        : settings.ADMINS[0][1],
    #~ 'FB'        : settings.FACEBOOK,
    #~ 'avisos'    : Aviso.objects.filter(mostrado=True)
#~ }


def sube_archivo_codigo(archivo_subido):
    nuevo_nombre = str(uuid.uuid1())+'.karel'
    with open(settings.RAIZ_CODIGOS+nuevo_nombre, 'wb+') as destino:
        for chunk in archivo_subido.chunks():
            destino.write(chunk)
    return nuevo_nombre


def index_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
        'noticias'  : Noticia.objects.all()
    }
    return render_to_response('inicio.html', data, context_instance=RequestContext(request))

def problemas_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True)
    }
    niveles = Nivel.objects.all()
    for nivel in niveles:
        nivel.problemas = nivel.problema_set.all()
        if request.user.is_authenticated():
            for problema in nivel.problemas:
                problema.mejor_puntaje_usuario = badgify(request.user.mejor_puntaje(problema))
    data['niveles'] = niveles
    return render_to_response('problemas.html', data, context_instance=RequestContext(request))

def problema_detalle(request, nombre_administrativo):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    problema = get_object_or_404(Problema, nombre_administrativo=nombre_administrativo, publico=True)
    if request.method == 'POST': #Recibimos un envío
        if request.user.is_authenticated():
            usuario = request.user
            archivo_codigo = settings.RAIZ_CODIGOS
            if 'codigo' in request.FILES:
                if request.FILES['codigo'].size < 22528:
                    archivo_codigo += sube_archivo_codigo(request.FILES['codigo'])
                else:
                    messages.warning(request, 'El archivo pesa demasiado, lo siento')
                    return HttpResponseRedirect('/problema/'+nombre_administrativo)
            else:
                archivo_codigo += str(uuid.uuid1())+'.karel'
                f = open(archivo_codigo, 'w')
                f.write(request.POST['codigo'].encode("utf-8"))
                f.close()
            envio = Envio(usuario=usuario, problema=problema, codigo_archivo=archivo_codigo, codigo=open(archivo_codigo, 'r').read(), ip=request.META['REMOTE_ADDR'])
            problema.veces_intentado += 1
            problema.save()
            envio.save()
            messages.success(request, 'Problema enviado, consulta tu calificación en la sección envíos (o espera a que se cargue el veredicto)')
            data['envio'] = envio.id
        else:
            messages.warning(request, 'Necesitas estar registrado para enviar soluciones')
    data['problema'] = problema
    data['js'] = ['js/excanvas.js', 'js/mundo.js', 'js/problema.js']
    if request.user.is_authenticated():
        data['mejor_puntaje'] = request.user.mejor_puntaje(problema)
        data['primer_puntaje'] = request.user.primer_puntaje(problema)
        data['intentos'] = request.user.intentos(problema)
        data['mejor_tiempo'] = request.user.mejor_tiempo(problema)
        data['usuarios_resuelto'] = request.user.usuarios_resuelto(problema)
        data['usuarios_intentado'] = request.user.usuarios_intentado(problema)
    return render_to_response('problema_detalle.html', data, context_instance=RequestContext(request))

@login_required
def envios_view(request):
    lista_envios = Envio.objects.filter(concurso=None)
    paginator = Paginator(lista_envios, 25)

    page = request.GET.get('pagina')
    try:
        envios = paginator.page(page)
    except PageNotAnInteger:
        envios = paginator.page(1)
    except EmptyPage:
        envios = paginator.page(paginator.num_pages)

    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['envios'] = envios
    data['js'] = ['js/envios.js']
    return render_to_response('envios.html', data, context_instance=RequestContext(request))

@login_required
def concursos_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'concursos' : Concurso.objects.filter(grupos__in=request.user.grupo.all(), fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now(), activo=True),
        'avisos'    : Aviso.objects.filter(mostrado=True),
        'concursos_todos': Concurso.objects.all()
    }
    for concurso in data['concursos']:
        diferencia = concurso.fecha_fin - timezone.now()
        concurso.quedan_dias    = ['', "%d días"%diferencia.days][diferencia.days!=0]
        horas = diferencia.seconds/3600
        concurso.quedan_horas   = ['', " %d horas"%horas][horas!=0]
        minutos = (diferencia.seconds/60)%60
        concurso.quedan_minutos = ['', " %d minutos"%minutos][minutos!=0]
        segundos = diferencia.seconds%60
        concurso.quedan_segundos = ['', ' %d segundos'%segundos][segundos!=0]
    return render_to_response('concursos.html', data, context_instance=RequestContext(request))

@login_required
def problema_concurso(request, id_concurso, id_problema):
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    problema = get_object_or_404(Problema, pk=id_problema)
    if problema in concurso.problemas.all() and concurso in Concurso.objects.filter(grupos__in=request.user.grupo.all(), fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now(), activo=True):
        data = {
            'path'          : request.path,
            'host'          : request.get_host(),
            'concurso'      : concurso,
            'problema'      : problema,
            'avisos'        : Aviso.objects.filter(mostrado=True),
            'mejor_puntaje' : request.user.mejor_puntaje(problema, concurso),
            'primer_puntaje': request.user.primer_puntaje(problema, concurso),
            'intentos'      : request.user.intentos(problema, concurso),
            'mejor_tiempo'  : request.user.mejor_tiempo(problema, concurso),
            'js'            : ['js/excanvas.js', 'js/mundo.js', 'js/problema.js']
        }
        if request.method == 'POST': #Recibimos un envío
            usuario = request.user
            archivo_codigo = settings.RAIZ_CODIGOS
            if 'codigo' in request.FILES:
                if request.FILES['codigo'].size < 22528:
                    archivo_codigo += sube_archivo_codigo(request.FILES['codigo'])
                else:
                    messages.warning(request, 'El archivo pesa demasiado, lo siento')
                    return HttpResponseRedirect('/concurso/%d/problema/%d'%(int(id_concurso), int(id_problema)))
            else:
                archivo_codigo += str(uuid.uuid1())+'.karel'
                f = open(archivo_codigo, 'w')
                f.write(request.POST['codigo'].encode("utf-8"))
                f.close()
            envio = Envio(usuario=usuario, problema=problema, concurso=concurso, codigo_archivo=archivo_codigo, codigo=open(archivo_codigo, 'r').read(), ip=request.META['REMOTE_ADDR'])
            envio.save()
            messages.success(request, 'Problema enviado, espera el veredicto')
            data['envio'] = envio.id
        return render_to_response('problema_concurso.html', data, context_instance=RequestContext(request))
    else:
        messages.error(request, '¡Hey! El tiempo para resolver este concurso terminó')
        return HttpResponseRedirect('/concurso/%d'%int(id_concurso))

@login_required
def concurso_view(request, id_concurso):
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    if concurso in Concurso.objects.filter(grupos__in=request.user.grupo.all(), fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now(), activo=True):
        diferencia = concurso.fecha_fin - timezone.now()
        concurso.quedan_dias    = ['', "%d días"%diferencia.days][diferencia.days!=0]
        horas = diferencia.seconds/3600
        concurso.quedan_horas   = ['', " %d horas"%horas][horas!=0]
        minutos = (diferencia.seconds/60)%60
        concurso.quedan_minutos = ['', " %d minutos"%minutos][minutos!=0]
        segundos = diferencia.seconds%60
        concurso.quedan_segundos = ['', ' %d segundos'%segundos][segundos!=0]

        participacion, creado = Participacion.objects.get_or_create(usuario=request.user, concurso=concurso)
        if creado:
            messages.success(request, 'Ahora estás participando en este concurso, ¡A darle!')

        concurso.lista_problemas = []
        for problema in concurso.problemas.all():
            problema.mejor_puntaje_usuario = badgify(request.user.mejor_puntaje(problema, concurso))
            concurso.lista_problemas.append(problema)

        data = {
            'path'      : request.path,
            'host'      : request.get_host(),
            'concurso'  : concurso,
            'avisos'    : Aviso.objects.filter(mostrado=True)
        }
        return render_to_response('concurso.html', data, context_instance=RequestContext(request))
    else:
        messages.error(request, 'Este concurso ya no está habilitado para ti')
        return HttpResponseRedirect('/concursos')

@login_required
def concurso_ver_ranking(request, id_concurso):
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    usuarios = []
    for participacion in Participacion.objects.filter(concurso=concurso).order_by('-puntaje'):
        usuario = participacion.usuario
        usuario.score = participacion.puntaje
        usuario.resultados = []
        for problema in concurso.problemas.all():
            usuario.resultados.append(badgify(usuario.mejor_puntaje(problema, concurso)))
        usuarios.append(usuario)
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'concurso'  : concurso,
        'usuarios'  : usuarios,
        'avisos'    : Aviso.objects.filter(mostrado=True)
    }
    return render_to_response('ranking.html', data, context_instance=RequestContext(request))

def medallero_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['path'] = request.path
    data['host'] = request.get_host()
    data['avisos'] = Aviso.objects.filter(mostrado=True)
    return render_to_response('medallero.html', data, context_instance=RequestContext(request))

def usuarios_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'usuarios'  : Usuario.objects.all().order_by('-puntaje'),
        'avisos'    : Aviso.objects.filter(mostrado=True)
    }
    if 'next' in request.GET:
        data['next'] = request.GET['next']
    return render_to_response('usuarios.html', data, context_instance=RequestContext(request))

@login_required
def usuario_view(request, id_usuario):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['usuario'] = Usuario.objects.get(pk=id_usuario)
    return render_to_response('usuario_ver.html', data, context_instance=RequestContext(request))

def wiki_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    return render_to_response('wiki.html', data, context_instance=RequestContext(request))

def ayuda_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    return render_to_response('ayuda.html', data, context_instance=RequestContext(request))

def privacidad_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    return render_to_response('privacidad.html', data, context_instance=RequestContext(request))

def registro_view(request):
    if not request.user.is_authenticated():
        data = {
            'GA'        : settings.GOOGLE_ANALYTHICS,
            'CA'        : settings.ADMINS[0][1],
            'FB'        : settings.FACEBOOK,
            'path'      : request.path,
            'host'      : request.get_host(),
            'avisos'    : Aviso.objects.filter(mostrado=True)
        }
        data['js'] = ['js/jquery-ui.js', 'js/registro.js']
        data['css'] = ['css/ui/jquery-ui.css']
        data['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        if request.method == 'POST':
            formulario = RegistroForm(request.POST)
            if formulario.is_valid():
                respuesta = verifica(settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'], request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'])
                if respuesta == True:
                    if request.POST['contrasenia'] == request.POST['repetir_contrasenia']:
                        nuevo_usario = formulario.save(commit=False)
                        nuevo_usario.set_password(request.POST['contrasenia'])
                        nuevo_usario.save()
                        nuevo_usario.grupo = request.POST.getlist('grupo')
                        nuevo_usario.save()
                        messages.success(request, 'Te has registrado correctamente')
                        return HttpResponseRedirect('/')
                    else:
                        messages.error(request, 'Las contraseñas no coinciden')
                else:
                    messages.error(request, 'Recaptcha dice que eres un robot: %s'%(respuesta))
            else:
                messages.error(request, 'Hay errores en algunos campos del formulario, verifica')
            data['formulario'] = formulario
            return render_to_response('registro.html', data, context_instance=RequestContext(request))
        else:
            data['formulario'] = RegistroForm()
            return render_to_response('registro.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Vamos, estás en una sesión, ¿Cómo pretendes registrarte?')
        return HttpResponseRedirect('/')

@login_required
def perfil_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['usuario'] = request.user
    data['asesorados'] = Usuario.objects.filter(asesor=request.user)
    if request.method == 'POST':
        formulario = PerfilForm(request.POST, instance=request.user)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Tus datos han sido actualizados')
        else:
            messages.error(request, 'Hay errores en algunos campos del formulario, verifica')
        data['formulario'] = formulario
        return render_to_response('perfil.html', data, context_instance=RequestContext(request))
    data['formulario'] = PerfilForm(instance=request.user)
    return render_to_response('perfil.html', data, context_instance=RequestContext(request))

@login_required
def mis_soluciones_view(request):
    lista_envios = Envio.objects.filter(concurso=None, usuario=request.user)
    paginator = Paginator(lista_envios, 25)

    page = request.GET.get('pagina')
    try:
        envios = paginator.page(page)
    except PageNotAnInteger:
        envios = paginator.page(1)
    except EmptyPage:
        envios = paginator.page(paginator.num_pages)

    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['envios'] = envios
    data['js'] = ['js/envios.js']
    return render_to_response('mis_soluciones.html', data, context_instance=RequestContext(request))

def faqs_view(request):
    data = {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK,
        'path'      : request.path,
        'host'      : request.get_host(),
        'avisos'    : Aviso.objects.filter(mostrado=True),
    }
    data['preguntas'] = PreguntaFrecuente.objects.filter(mostrado=True)
    return render_to_response('faqs.html', data, context_instance=RequestContext(request))

def login(request):
    if not request.user.is_authenticated():
        if 'correo' in request.POST and 'pass' in request.POST and 'redirect' in request.POST:
            username = request.POST['correo']
            password = request.POST['pass']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, '¡¡Hola de vuelta!!')
                    return HttpResponseRedirect(request.POST['redirect'])
                else:
                    messages.error(request, 'Por razones que trascienden la escolástica, tu cuenta está desactivada')
            else:
                messages.error(request, 'Nadie registrado con ese correo, ¿Y si verificas?')
            return HttpResponseRedirect(request.POST['redirect'])
        else:
            messages.warning(request, '¡Hey hey hey! ¡Faltan los campos del formulario!')
            return HttpResponseRedirect('/')
    else:
        messages.warning(request, '¿No ya estabas dentro? %s'%request.user)
        return HttpResponseRedirect('/')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Nos vemos pronto')
    return HttpResponseRedirect('/')

@login_required
def internal_change_pass(request):
    oldpass     = request.POST['old']
    pass1       = request.POST['pass1']
    pass2       = request.POST['pass2']
    if pass1==pass2:
        if auth.authenticate(username=request.user.correo, password=oldpass):
            request.user.set_password(pass1)
            request.user.save()
            messages.success(request, 'Password cambiado')
            return HttpResponseRedirect('/perfil')
        else:
            messages.warning(request, 'Tu contraseña anterior no es la bena')
            return HttpResponseRedirect('/perfil')
    else:
        messages.warning(request, '¡Las contraseñas no coinciden!')
        return HttpResponseRedirect('/perfil')

@login_required
def external_change_pass(request):
    if request.user.has_perm('apps.usuarios.can_change_usuario'):
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1==pass2:
            u = Usuario.objects.get(pk=request.POST['usuario'])
            u.set_password(pass1)
            u.save()
            messages.success(request, 'Password cambiado')
            return HttpResponseRedirect(request.POST['redirect'])
        else:
            messages.warning(request, '¡Las contraseñas no coinciden!')
            return HttpResponseRedirect(request.POST['redirect'])
    else:
        messages.error(request, '¡No tienes permiso de realizar esta acción!')
        return HttpResponseRedirect('/')

@login_required
def baja(request):
    """Procesa la baja del sistema"""
    request.user.delete()
    messages.warning(request, 'Chau, esperamos verte pronto')
    return HttpResponseRedirect('/')
