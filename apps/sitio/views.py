# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import messages
import django.contrib.auth as auth
from apps.sitio.models import Aviso, Noticia, PreguntaFrecuente
from apps.evaluador.models import Nivel, Problema, Concurso
from apps.usuarios.models import Usuario

data = {
    'GA'        : settings.GOOGLE_ANALYTHICS,
    'CA'        : settings.ADMINS[0][1],
    'FB'        : settings.FACEBOOK,
    'avisos'    : Aviso.objects.filter(mostrado=True)
}

def index_view(request):
    data['path'] = request.path
    data['noticias'] = Noticia.objects.all()
    return render_to_response('inicio.html', data, context_instance=RequestContext(request))

def problemas_view(request):
    data['path'] = request.path
    data['niveles'] = Nivel.objects.all()
    return render_to_response('problemas.html', data, context_instance=RequestContext(request))

def problema_detalle(request, nombre_administrativo):
    data['path'] = request.path
    data['problema'] = get_object_or_404(Problema, nombre_administrativo=nombre_administrativo, publico=True)
    data['js'] = ['js/mundo.js', 'js/problema.js']
    return render_to_response('problema_detalle.html', data, context_instance=RequestContext(request))

def envios_view(request):
    data['path'] = request.path
    data['concursos'] = request.path
    return render_to_response('envios.html', data, context_instance=RequestContext(request))

def concursos_view(request):
    if request.user.is_authenticated():
        data['path'] = request.path
        data['concursos'] = Concurso.objects.all()
        return render_to_response('concursos.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Debes iniciar sesión para ver los concursos')
        return HttpResponseRedirect('/')

def concurso_participar(request):
    if request.user.is_authenticated():
        pass
    else:
        messages.warning(request, 'Debes iniciar sesión para ver los concursos')
        return HttpResponseRedirect('/')

def concurso_ver_ranking(request, id_concurso):
    if request.user.is_authenticated():
        pass
    else:
        messages.warning(request, 'Debes iniciar sesión para ver los concursos')
        return HttpResponseRedirect('/')

def medallero_view(request):
    data['path'] = request.path
    return render_to_response('medallero.html', data, context_instance=RequestContext(request))

def usuarios_view(request):
    data['path'] = request.path
    data['usuarios'] = Usuario.objects.all()
    return render_to_response('usuarios.html', data, context_instance=RequestContext(request))

def usuario_view(request, id_usuario):
    data['path'] = request.path
    data['usuario'] = Usuario.objects.get(pk=id_usuario)
    return render_to_response('usuario_ver.html', data, context_instance=RequestContext(request))

def wiki_view(request):
    data['path'] = request.path
    return render_to_response('wiki.html', data, context_instance=RequestContext(request))

def ayuda_view(request):
    data['path'] = request.path
    return render_to_response('ayuda.html', data, context_instance=RequestContext(request))

def privacidad_view(request):
    data['path'] = request.path
    return render_to_response('privacidad.html', data, context_instance=RequestContext(request))

def registro_view(request):
    if not request.user.is_authenticated():
        data['path'] = request.path
        return render_to_response('registro.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, 'Vamos, estás en una sesión, ¿Cómo pretendes registrarte?')

def perfil_view(request):
    if request.user.is_authenticated():
        data['path'] = request.path
        data['usuario'] = request.user
        return render_to_response('perfil.html', data, context_instance=RequestContext(request))
    else:
        messages.error(request, 'No has iniciado sesión...¿Qué perfil te voy a mostrar?')
        return HttpResponseRedirect('/')

def mis_soluciones_view(request):
    if request.user.is_authenticated():
        data['path'] = request.path
        data['usuario'] = request.user
        return render_to_response('mis_soluciones.html', data, context_instance=RequestContext(request))
    else:
        messages.error(request, 'No has iniciado sesión...¿Qué te voy a mostrar?')
        return HttpResponseRedirect('/')

def faqs_view(request):
    data['path'] = request.path
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

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        messages.success(request, 'Nos vemos pronto')
        return HttpResponseRedirect('/')
    else:
        messages.warning(request, 'Aguanta, no iniciaste sesión o ya habías salido...')
        return HttpResponseRedirect('/')

def external_change_pass(request):
    if request.user.is_authenticated():
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
    else:
        messages.error(request, '¡Qué pretendes!')
        return HttpResponseRedirect('/')