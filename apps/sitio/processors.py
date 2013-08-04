# -*- coding:utf-8 -*-
# Archivo de procesadores para el sistema de templates de django
from django.conf import settings
from apps.sitio.models import Aviso

def settings_processor(request):
    return {
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK
    }

def path_processor(request):
    return {'path': request.path}

def avisos_processor(request):
    return {'avisos': Aviso.objects.filter(mostrado=True)}
