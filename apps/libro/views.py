# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apps.libro.models import Libro, Codigo, Capitulo
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.usuarios.models import Grupo, Usuario
from django.contrib import messages
from django_downloadview import ObjectDownloadView
from functools import wraps

### wrapers
def requiere_compra(vista):
    """forza una vista a recibir el valor indicado por post"""
    @wraps(vista)
    def wrapper(*args, **kwds):
        request = args[0]
        capitulo = get_object_or_404(Capitulo, pk=kwds['pk'])
        if capitulo.libro in request.user.libros.all():
            return vista(*args, **kwds)
        else:
            messages.warning(request, 'no has comprado este libro')
            return HttpResponseRedirect('/material')
    return wrapper
### endwrapers

@require_POST
@login_required
def activa_codigo(request):
    codigo = get_object_or_404(Codigo, codigo=request.POST.get('codigo', ''), usado=False)
    codigo.usado = True
    codigo.fecha_activacion = timezone.now()
    codigo.usuario = request.user
    codigo.save()

    codigo.libro.lectores.add(request.user)
    codigo.libro.save()

    grupo_libro = Grupo.objects.get_or_create(nombre=codigo.libro.grupo)[0]
    request.user.perfil.grupos.add(grupo_libro)
    request.user.perfil.save()
    messages.success(request, 'Libro %s activado, ahora puedes descargar los capítulos'%codigo.libro)
    return HttpResponseRedirect(request.POST.get('next', '/perfil'))

def material(request):
    data = {
        'libros': Libro.objects.all()
    }
    return render_to_response('libro/material.html', data, context_instance=RequestContext(request))

@login_required
def libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    grupo = Grupo.objects.get_or_create(nombre=libro.grupo)[0]
    if grupo in request.user.perfil.grupos.all():
        data = {
            'libro': libro
        }
        return render_to_response('libro/libro.html', data, context_instance=RequestContext(request))
    else:
        messages.warning(request, '¡No has comprado este libro!')
        return HttpResponseRedirect('/material')

descargar_capitulo = requiere_compra(login_required(ObjectDownloadView.as_view(model=Capitulo, file_field='archivo')))

#~ @login_required
#~ def descargar_capitulo(request, id_capitulo):
    #~ capitulo = get_object_or_404(Capitulo, pk=id_capitulo)
    #~ grupo = Grupo.objects.get_or_create(nombre=capitulo.libro.grupo)[0]
    #~ if grupo in request.user.perfil.grupos.all():
        #~ pass
        #~ #forzar la descarga
    #~ else:
        #~ messages.warning(request, '¡No has comprado este libro!')
        #~ return HttpResponseRedirect('/material')
