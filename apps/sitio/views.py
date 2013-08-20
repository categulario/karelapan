# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from apps.evaluador.models import Nivel, Problema, Concurso, Envio, Participacion, Consulta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.usuarios.models import Usuario, Grupo
from modules.recaptcha import verifica
from apps.sitio.models import Aviso, Noticia, PreguntaFrecuente
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail, EmailMessage, mail_admins
from apps.usuarios.forms import RegistroForm, PerfilForm
from django.template import RequestContext
from modules.badges import badgify
from django.contrib import messages
from django.contrib import auth
from modules.fechas import diferencia_str
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid1
from functools import wraps

import datetime
import uuid

### wrappers
def permiso_o_grupo_concurso(permiso):
    """forza una vista a requerir un permiso o pertenecer a un grupo"""
    def envoltura(vista):
        @wraps(vista)
        def wrapper(*args, **kwds):
            request = args[0]
            if request.user.is_authenticated():
                concurso = Concurso.objects.get(pk=kwds['id_concurso'])
                grupo = concurso.administradores
                if grupo in request.user.groups.all() or request.user.has_perm(permiso):
                    return vista(*args, **kwds)
            response =  HttpResponse('No tienes permitida esta acción', content_type='text/plain')
            response.status_code=403
            return response
        return wrapper
    return envoltura
### endwrappers

def sube_archivo_codigo(archivo_subido):
    nuevo_nombre = str(uuid.uuid1())+'.karel'
    with open(settings.RAIZ_CODIGOS+nuevo_nombre, 'wb+') as destino:
        for chunk in archivo_subido.chunks():
            destino.write(chunk)
    return nuevo_nombre

def channel(request):
    return HttpResponse('<script src="//connect.facebook.net/en_US/all.js"></script>')

def index_view(request):
    data = {
        'noticias'  : Noticia.objects.all()
    }
    return render_to_response('inicio.html', data, context_instance=RequestContext(request))

def problemas_view(request):
    data = {}
    niveles = Nivel.objects.all()
    for nivel in niveles:
        nivel.problemas = nivel.problema_set.filter(publico=True)
        if request.user.is_authenticated():
            for problema in nivel.problemas:
                problema.mejor_puntaje_usuario = badgify(Usuario.objects.get(pk=request.user.id).mejor_puntaje(problema))
    data['niveles'] = niveles
    return render_to_response('problemas.html', data, context_instance=RequestContext(request))

def problema_detalle(request, nombre_administrativo):
    data = {}
    problema = get_object_or_404(Problema, nombre_administrativo=nombre_administrativo, publico=True)
    if request.method == 'POST': #Recibimos un envío
        if request.user.is_authenticated():
            usuario = Usuario.objects.get(pk=request.user.id)
            if not usuario.participa_en_concurso():
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
                messages.warning(request, 'No puedes enviar soluciones al problemario mientras estás en un concurso')
        else:
            messages.warning(request, 'Necesitas estar registrado para enviar soluciones')
    data['problema'] = problema
    data['js'] = ['js/mundo.js', 'js/problema.js']
    if request.user.is_authenticated():
        usuario = Usuario.objects.get(pk=request.user.id)
        data['mejor_puntaje'] = usuario.mejor_puntaje(problema)
        data['primer_puntaje'] = usuario.primer_puntaje(problema)
        data['intentos'] = usuario.intentos(problema)
        data['mejor_tiempo'] = usuario.mejor_tiempo(problema)
        data['usuarios_resuelto'] = usuario.usuarios_resuelto(problema)
        data['usuarios_intentado'] = usuario.usuarios_intentado(problema)
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

    data = {}
    data['envios'] = envios
    data['js'] = ['js/envios.js']
    return render_to_response('envios.html', data, context_instance=RequestContext(request))

@login_required
def concursos_view(request):
    lista_concursos = Concurso.objects.all()
    paginator = Paginator(lista_concursos, 5)

    page = request.GET.get('pagina')
    try:
        concursos = paginator.page(page)
    except PageNotAnInteger:
        concursos = paginator.page(1)
    except EmptyPage:
        concursos = paginator.page(paginator.num_pages)
    data = {
        'concursos' : Usuario.objects.get(pk=request.user.id).concursos_activos_y_futuros()
    }
    if request.user.has_perm('evaluador.puede_ver_ranking'):
        data['concursos_todos'] = concursos
    for concurso in data['concursos']:
        if concurso.en_curso:
            concurso.tiempo_restante = diferencia_str(concurso.fecha_fin)
        else:
            concurso.tiempo_restante = diferencia_str(concurso.fecha_inicio)
    return render_to_response('concursos.html', data, context_instance=RequestContext(request))

@login_required
def problema_concurso(request, id_concurso, id_problema):
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    problema = get_object_or_404(Problema, pk=id_problema)
    usuario = Usuario.objects.get(pk=request.user.id)
    if problema in concurso.problemas.all() and concurso in usuario.concursos_activos():
        data = {
            'concurso'          : concurso,
            'problema'          : problema,
            'mejor_puntaje'     : usuario.mejor_puntaje(problema, concurso),
            'primer_puntaje'    : usuario.primer_puntaje(problema, concurso),
            'intentos'          : usuario.intentos(problema, concurso),
            'mejor_tiempo'      : usuario.mejor_tiempo(problema, concurso),
            'consultas'         : Consulta.objects.filter(usuario=usuario, problema=problema, concurso=concurso, leido=True),
            'tiempo_restante_consultas': diferencia_str(concurso.fecha_inicio + datetime.timedelta(minutes=concurso.duracion_preguntas)),
            'permite_consultas' : usuario.puede_hacer_consulta(concurso),
            'js'                : ['js/excanvas.js', 'js/mundo.js', 'js/problema.js', 'js/problema_concurso.js']
        }
        if request.method == 'POST': #Recibimos un envío
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
    usuario = Usuario.objects.get(pk=request.user.id)
    if concurso in usuario.concursos_activos():
        diferencia = concurso.fecha_fin - timezone.now()
        concurso.quedan_dias    = ['', "%d días"%diferencia.days][diferencia.days!=0]
        horas = diferencia.seconds/3600
        concurso.quedan_horas   = ['', " %d horas"%horas][horas!=0]
        minutos = (diferencia.seconds/60)%60
        concurso.quedan_minutos = ['', " %d minutos"%minutos][minutos!=0]
        segundos = diferencia.seconds%60
        concurso.quedan_segundos = ['', ' %d segundos'%segundos][segundos!=0]

        participacion, creado = Participacion.objects.get_or_create(usuario=usuario, concurso=concurso, primera_ip=request.META['REMOTE_ADDR'])
        if creado:
            messages.success(request, 'Ahora estás participando en este concurso, ¡A darle!')

        concurso.lista_problemas = []
        for problema in concurso.problemas.all():
            problema.mejor_puntaje_usuario = badgify(usuario.mejor_puntaje(problema, concurso))
            concurso.lista_problemas.append(problema)

        data = {
            'concurso'  : concurso
        }
        return render_to_response('concurso.html', data, context_instance=RequestContext(request))
    else:
        messages.error(request, 'Este concurso ya no está habilitado para ti')
        return HttpResponseRedirect('/concursos')

@permiso_o_grupo_concurso('evaluador.administrar_todos_concursos')
def concurso_ver_ranking(request, id_concurso):
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    usuarios = []
    for participacion in Participacion.objects.filter(concurso=concurso).order_by('-puntaje'):
        usuario = participacion.usuario
        usuario.score = participacion.puntaje
        usuario.resultados = []
        for problema in concurso.problemas.all():
            usuario.resultados.append(badgify(Usuario(usuario).mejor_puntaje(problema, concurso)))
        usuarios.append(usuario)
    data = {
        'concurso'  : concurso,
        'usuarios'  : usuarios
    }
    return render_to_response('ranking.html', data, context_instance=RequestContext(request))

@login_required
def concurso_ver_ranking_publico(request, id_concurso):
    concurso = get_object_or_404(Concurso, pk=id_concurso, ranking_publico=True)
    usuarios = []
    for participacion in Participacion.objects.filter(concurso=concurso).order_by('-puntaje'):
        usuario = participacion.usuario
        usuario.score = participacion.puntaje
        usuario.resultados = []
        for problema in concurso.problemas.all():
            usuario.resultados.append(badgify(Usuario(usuario).mejor_puntaje(problema, concurso)))
        usuarios.append(usuario)
    data = {
        'concurso'  : concurso,
        'usuarios'  : usuarios
    }
    return render_to_response('ranking.html', data, context_instance=RequestContext(request))

@permiso_o_grupo_concurso('evaluador.administrar_todos_concursos')
def concurso_ver_consultas(request, id_concurso):
    """Muesta las consultas hechas por los usuarios"""
    concurso = get_object_or_404(Concurso, pk=id_concurso)
    data = {
        'consultas' : Consulta.objects.filter(concurso=concurso),
        'concurso'  : concurso,
        'js'        : ['js/consultas.js']
    }
    return render_to_response('consultas.html', data, context_instance=RequestContext(request))

@login_required
def medallero_view(request):
    data = {
        'usuarios': Usuario.objects.order_by('-perfil__puntaje').filter(perfil__inscripciones__anio=settings.OLIMPIADA_ACTUAL)[:30],
        'concursos': Concurso.objects.filter(olimpiada__anio=settings.OLIMPIADA_ACTUAL, ranking_publico=True).order_by('-fecha_inicio')
    }
    return render_to_response('medallero.html', data, context_instance=RequestContext(request))

def usuarios_view(request):
    lista_usuarios = Usuario.objects.all().order_by('perfil__nombre_completo')
    paginator = Paginator(lista_usuarios, 50)

    page = request.GET.get('pagina')
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)
    data = {
        'usuarios'  : usuarios,
        'cuenta': Usuario.objects.count()
    }
    if 'next' in request.GET:
        data['next'] = request.GET['next']
    return render_to_response('usuarios.html', data, context_instance=RequestContext(request))

@login_required
def usuario_view(request, nombre_usuario):
    data = {
        'usuario': get_object_or_404(Usuario, username=nombre_usuario)
    }
    return render_to_response('usuario_ver.html', data, context_instance=RequestContext(request))

def wiki_view(request):
    data = {}
    return render_to_response('wiki.html', data, context_instance=RequestContext(request))

def ayuda_view(request):
    data = {}
    return render_to_response('ayuda.html', data, context_instance=RequestContext(request))

def privacidad_view(request):
    data = {}
    return render_to_response('privacidad.html', data, context_instance=RequestContext(request))

def registro_view(request):
    if not request.user.is_authenticated():
        data = {}
        data['js'] = ['js/jquery-ui.js', 'js/registro.js']
        data['css'] = ['css/ui/jquery-ui.css', 'css/recaptcha.css']
        data['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        if request.method == 'POST':
            formulario = RegistroForm(request.POST)
            if formulario.is_valid():
                respuesta = verifica(settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'], request.POST.get('recaptcha_challenge_field', '').encode('utf8'), request.POST.get('recaptcha_response_field', '').encode('utf8'))
                if respuesta == True:
                    if request.POST['contrasenia'] == request.POST['repetir_contrasenia']:
                        nuevo_usuario = Usuario(username=request.POST.get('nombre_de_usuario') ,email=request.POST.get('correo'), is_active=False)
                        nuevo_usuario.set_password(request.POST.get('contrasenia'))
                        nuevo_usuario.save()

                        perfil = formulario.save(commit=False)
                        token_confirmacion = str(uuid1())
                        perfil.confirm_token = token_confirmacion
                        try:
                            id_asesor = int(request.POST.get('asesor'))
                            perfil.asesor = Usuario.objects.get(pk=id_asesor)
                        except ValueError:
                            perfil.asesor = None
                        perfil.usuario = nuevo_usuario
                        perfil.nombre_completo = "%s %s %s"%(request.POST.get('nombre'),request.POST.get('appat'),request.POST.get('apmat'))
                        perfil.save()
                        perfil.grupos = [Grupo.objects.get_or_create(nombre='usuarios')[0], Grupo.objects.get_or_create(nombre=request.POST.get('subsistema'))[0]]
                        perfil.save()
                        data = {
                            'token': token_confirmacion,
                            'correo': nuevo_usuario.email
                        }
                        msg = EmailMessage(
                            'Confirma tu correo electrónico',
                            render_to_string('mail/confirma.html', data, context_instance=RequestContext(request)),
                            'Karelapan <karelapan@gmail.com>',
                            [nuevo_usuario.email]
                        )
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                        mail_admins('Nuevo registro', 'Se ha registrado un usuario con el nombre %s en la fecha %s'%(perfil.nombre_completo, nuevo_usuario.date_joined))
                        messages.success(request, 'Te has registrado correctamente, revisa tu correo para verificar tu cuenta')
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
    usuario = Usuario.objects.get(pk=request.user.id)
    data = {
        'usuario': usuario,
        'asesorados': Usuario.objects.filter(perfil__asesor=usuario)
    }
    if request.method == 'POST':
        formulario = PerfilForm(request.POST, instance=usuario.perfil)
        if formulario.is_valid():
            perfil = formulario.save(commit=False)
            perfil.nombre_completo = "%s %s %s"%(request.POST.get('nombre'), request.POST.get('appat'), request.POST.get('apmat'))
            try:
                id_asesor = int(request.POST.get('asesor'))
                perfil.asesor = Usuario.objects.get(pk=id_asesor)
            except ValueError:
                perfil.asesor = None
            perfil.save()
            messages.success(request, 'Tus datos han sido actualizados')
        else:
            messages.error(request, 'Hay errores en algunos campos del formulario, verifica')
        data['js'] = ['js/perfil.js']
        data['formulario'] = formulario
        return render_to_response('perfil.html', data, context_instance=RequestContext(request))
    data['formulario'] = PerfilForm(instance=usuario.perfil)
    data['js'] = ['js/perfil.js']
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

    data = {}
    data['envios'] = envios
    data['js'] = ['js/envios.js']
    return render_to_response('mis_soluciones.html', data, context_instance=RequestContext(request))

def faqs_view(request):
    data = {
        'preguntas': PreguntaFrecuente.objects.filter(mostrado=True)
    }
    return render_to_response('faqs.html', data, context_instance=RequestContext(request))

def soporte(request):
    return render_to_response('soporte.html', context_instance=RequestContext(request))

def login(request):
    if not request.user.is_authenticated():
        if 'correo' in request.POST and 'pass' in request.POST and 'redirect' in request.POST:
            username = request.POST['correo']
            password = request.POST['pass']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    user.perfil.confirm_token = None
                    user.perfil.save()
                    messages.success(request, '¡¡Hola de vuelta!!')
                    return HttpResponseRedirect(request.POST['redirect'])
                else:
                    messages.error(request, 'Por razones que trascienden la escolástica, tu cuenta está desactivad. ¿Verificaste tu correo electrónico?')
            else:
                messages.error(request, 'Nadie registrado con ese usuario, ¿Y si verificas?')
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
        if auth.authenticate(username=request.user.username, password=oldpass):
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

def confirma_correo(request, correo, token):
    """Confirma el correo electrónico de un usuario"""
    usuario = get_object_or_404(Usuario, email=correo)
    if usuario.perfil.confirm_token == token:
        usuario.is_active = True
        usuario.perfil.confirm_token = None
        usuario.save()
        usuario.perfil.save()
        data = {
            'js': ['js/excanvas.js', 'js/mundo.js', 'js/bienvenida.js']
        }
        messages.success(request, 'Has verificado tu correo electrónico con éxito')
        return render_to_response('correo_confirmado.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Ya habías verificado tu cuenta, no puedes hacerlo de nuevo')
        return HttpResponseRedirect('/')

def recuperar_contrasenia(request):
    """Muestra la pantalla de recuperación de contraseña"""
    data = {'css':  ['css/recaptcha.css']}
    if not request.user.is_authenticated():
        data['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        if request.method == 'POST':
            respuesta = verifica(settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'], request.POST.get('recaptcha_challenge_field', '').encode('utf-8'), request.POST.get('recaptcha_response_field', '').encode('utf-8'))
            if respuesta == True:
                usuario = get_object_or_404(Usuario, email=request.POST.get('correo'))
                token_confirmacion = str(uuid1())
                usuario.perfil.confirm_token = token_confirmacion
                usuario.perfil.save()
                dat = {
                    'token': token_confirmacion,
                    'nombre_usuario': usuario.username,
                    'correo': usuario.email
                }
                msg = EmailMessage(
                    'Recuperación de contraseña',
                    render_to_string('mail/recupera.html', dat, context_instance=RequestContext(request)),
                    'Karelapan <karelapan@gmail.com>',
                    [usuario.email]
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                messages.success(request, 'Se ha enviado un enlace a tu correo electrónico para recuperar la contraseña')
            else:
                messages.error(request, 'Recaptcha dice que eres un robot: %s'%(respuesta))
            return render_to_response('recuperar_contrasenia.html', data, context_instance=RequestContext(request))
        else:
            return render_to_response('recuperar_contrasenia.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Vamos, estás en una sesión, ¿Cómo perdiste tu contraseña?')
        return HttpResponseRedirect('/')

def confirma_recuperacion(request, correo, token):
    """Muestra el diálogo de recuperar contraseña"""
    if not request.user.is_authenticated():
        data = {
            'usuario': get_object_or_404(Usuario, email=correo, perfil__confirm_token=token)
        }
        if request.method == 'POST':
            contrasenia = request.POST.get('pass')
            contrasenia_confirmar = request.POST.get('pass-repeat')
            if contrasenia == contrasenia_confirmar and contrasenia != '':
                data['usuario'].set_password(contrasenia)
                data['usuario'].save()
                data['usuario'].perfil.confirm_token = None
                data['usuario'].perfil.save()
                messages.success(request, '¡Ya tienes nueva contraseña!')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Las contraseñas no coinciden o están vacías')
        return render_to_response('confirma_contrasenia.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Vamos, estás en una sesión, ¿Cómo perdiste tu contraseña?')
        return HttpResponseRedirect('/')


@csrf_exempt
def error404(request):
    return render_to_response('errors/404.html', context_instance=RequestContext(request))

def error500(request):
    return render_to_response('errors/500.html', context_instance=RequestContext(request))

def error403(request):
    return render_to_response('errors/403.html', context_instance=RequestContext(request))

def test(request):
    """Confirma el correo electrónico de un usuario"""
    data = {
        'js': ['js/excanvas.js', 'js/mundo.js', 'js/bienvenida.js']
    }
    return render_to_response('correo_confirmado.html', data, context_instance=RequestContext(request))
