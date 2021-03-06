# -*- coding:utf-8 -*-
# Archivo de procesadores para el sistema de templates de django
from django.conf import settings
from apps.sitio.models import Aviso
from apps.usuarios.models import Usuario
from django.utils import timezone

def settings_processor(request):
    return {
        'host'      : settings.BASE_URL,
        'GA'        : settings.GOOGLE_ANALYTHICS,
        'CA'        : settings.ADMINS[0][1],
        'FB'        : settings.FACEBOOK
    }

def path_processor(request):
    return {'path': request.path}

def avisos_processor(request):
    return {'avisos': Aviso.objects.filter(mostrado=True, caducidad__gte=timezone.now())}

def concursos_processor(request):
    """Indica si un usuario tiene concursos activos"""
    if request.user.is_authenticated():
        u = Usuario.objects.get(pk=request.user.id)
        return {'tiene_concursos': u.participa_en_concurso() and not u.en_concurso()}
    else:
        return {'tiene_concursos': False}
