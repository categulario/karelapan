# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def inicio(request):
    return render_to_response('karelecatl/template.html', context_instance=RequestContext(request))
