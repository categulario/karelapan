from django.conf.urls import patterns,url
from feed import UltimosProblemas

urlpatterns = patterns('apps.libro.views',
    url(r'^$', 'material'),
    url(r'^libro/(?P<id_libro>\d+)/$', 'libro'),
    url(r'^activar/$', 'activa_codigo')
)
