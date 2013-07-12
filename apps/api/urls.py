from django.conf.urls import patterns,url

urlpatterns = patterns('apps.api.views',
    url(r'^$', 'index'),
    url(r'^mundo_ejemplo/(?P<id_problema>\d+)/$', 'mundo_ejemplo'),
    url(r'^mundo_ejemplo_solucion/(?P<id_problema>\d+)/$', 'mundo_ejemplo_solucion'),
    url(r'^nombres_escuela/$', 'nombres_escuela'),
    url(r'^descarga_codigo/(?P<id_envio>\d+)/$', 'descarga_codigo'),
    url(r'^envio/(?P<id_envio>\d+)/$', 'envio'),
    url(r'^envio/(?P<id_envio>\d+)/concurso/(?P<id_concurso>\d+)/$', 'envio'),
    url(r'^hacer_consulta/$', 'hacer_consulta'),
    url(r'^responde_consulta/$', 'responde_consulta'),
    url(r'^busca_consultas/(?P<id_concurso>\d+)/$', 'busca_consultas'),
)
