from django.conf.urls import patterns,url
from feed import UltimosProblemas
from django.conf import settings

urlpatterns = patterns('apps.sitio.views',
    url(r'^$', 'index_view'),
    url(r'^envios/$', 'envios_view'),
    url(r'^concursos/$', 'concursos_view'),
    url(r'^concurso/(?P<id_concurso>\d+)/$', 'concurso_view'),
    url(r'^concurso/(?P<id_concurso>\d+)/ranking/$', 'concurso_ver_ranking'),
    url(r'^concurso/(?P<id_concurso>\d+)/ranking/public/$', 'concurso_ver_ranking_publico'),
    url(r'^concurso/(?P<id_concurso>\d+)/consultas/$', 'concurso_ver_consultas'),
    url(r'^concurso/(?P<id_concurso>\d+)/problema/(?P<id_problema>\d+)/$', 'problema_concurso'),
    url(r'^medallero/$', 'medallero_view'),
    url(r'^faqs/$', 'faqs_view'),
    url(r'^soporte/$', 'soporte'),
    url(r'^ayuda/$', 'ayuda_view'),
    url(r'^privacidad/$', 'privacidad_view'),
    url(r'^perfil/$', 'perfil_view'),
    url(r'^registro/$', 'registro_view'),
    url(r'^mis_soluciones/$', 'mis_soluciones_view'),
    url(r'^usuarios/$', 'usuarios_view'),
    url(r'^usuario/(?P<nombre_usuario>[a-zA-Z0-9-_.+@]+)$', 'usuario_view'),
    url(r'^problemas/$', 'problemas_view'),
    url(r'^problema/(?P<nombre_administrativo>[a-zA-Z0-9_-]+)/$', 'problema_detalle'),
    url(r'^auth/login/$', 'login'),
    url(r'^auth/logout/$', 'logout'),
    url(r'^auth/change_pass/$', 'external_change_pass'),
    url(r'^auth/change_pass_internal/$', 'internal_change_pass'),
    url(r'^baja/$', 'baja'),
    url(r'^problemas/feed/$', UltimosProblemas()),
    url(r'^verifica/(?P<correo>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})/token/(?P<token>[a-z0-9-]+)/', 'confirma_correo'),
    url(r'^recuperar_contrasenia/', 'recuperar_contrasenia'),
    url(r'^confirma_recuperacion/(?P<correo>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})/token/(?P<token>[a-z0-9-]+)/', 'confirma_recuperacion'),
    url(r'^exportar/', 'exportar'),
)

if settings.DEBUG:
    urlpatterns += patterns('apps.sitio.views',
        url(r'^test/', 'test'),
    )