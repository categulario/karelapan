from django.conf.urls import patterns,url

urlpatterns = patterns('apps.sitio.views',
    url(r'^$', 'index_view'),
    url(r'^envios/$', 'envios_view'),
    url(r'^concursos/$', 'concursos_view'),
    url(r'^concursos/participar$', 'concurso_participar'),
    url(r'^concurso/ver_ranking/(?P<id_concurso>\d+)/$', 'concurso_ver_ranking'),
    url(r'^medallero/$', 'medallero_view'),
    url(r'^faqs/$', 'faqs_view'),
    url(r'^wiki/$', 'wiki_view'),
    url(r'^ayuda/$', 'ayuda_view'),
    url(r'^privacidad/$', 'privacidad_view'),
    url(r'^perfil/$', 'perfil_view'),
    url(r'^registro/$', 'registro_view'),
    url(r'^mis_soluciones/$', 'mis_soluciones_view'),
    url(r'^usuarios/$', 'usuarios_view'),
    url(r'^usuario/(?P<id_usuario>\d+)$', 'usuario_view'),
    url(r'^problemas/$', 'problemas_view'),
    url(r'^problema/(?P<nombre_administrativo>\w+)/$', 'problema_detalle'),
    url(r'^auth/login/$', 'login'),
    url(r'^auth/logout/$', 'logout'),
    url(r'^auth/change_pass/$', 'external_change_pass'),
    url(r'^auth/change_pass_internal/$', 'internal_change_pass'),
    url(r'^baja/$', 'baja'),
)
