# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apps.libro.models import Libro, Codigo
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.usuarios.models import Grupo, Usuario
from django.contrib import messages

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

#TODO proteger esta vista
def libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    data = {
        'libro': libro
    }
    return render_to_response('libro/libro.html', data, context_instance=RequestContext(request))
