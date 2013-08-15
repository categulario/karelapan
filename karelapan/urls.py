from django.conf.urls import patterns, include, url
from wiki.urls import get_pattern as get_wiki_pattern
from django_notify.urls import get_pattern as get_notify_pattern
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('apps.sitio.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^karelecatl/', include('apps.karelecatl.urls')),
    url(r'^channel.html', 'apps.sitio.views.channel'),
)

urlpatterns += patterns('',
    (r'^notify/', get_notify_pattern()),
    (r'^wiki/', get_wiki_pattern())
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve'),
        url(r'^404/$', 'apps.sitio.views.error404'),
        url(r'^403/$', 'apps.sitio.views.error403'),
        url(r'^500/$', 'apps.sitio.views.error500'),
    )
