# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apps.libro.models import Libro
from django.views.decorators.http import require_POST

@require_POST
def activa_codigo(request):
    return HttpResponse('ok')

def material(request):
    data = {
        'libros': Libro.objects.all()
    }
    return render_to_response('libro/material.html', data, context_instance=RequestContext(request))

def libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    data = {
        'libro': libro
    }
    return render_to_response('libro/libro.html', data, context_instance=RequestContext(request))
