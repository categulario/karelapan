# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from apps.evaluador.models import Problema, Nivel
from django.conf import settings
import datetime

class UltimosProblemas(Feed):
    title = "Problemas en Karelapan.com"
    link = "/problemas/"
    description = "Últimos problemas añadidios al set de problemas de Karelapan"
    subtitle = "Últimos problemas añadidios al set de problemas de Karelapan"
    feed_url = '/problemas/feed/'
    author_name = '@Categulario'
    author_email = settings.ADMINS[0][1]
    author_link = 'https://twitter.com/categulario'

    def items(self):
        return Problema.objects.order_by('-fecha_publicacion')[:10]

    def item_title(self, item):
        return item.nombre

    def item_description(self, item):
        return item.descripcion

    def item_link(self, item):
        return reverse('apps.sitio.views.problema_detalle', args=[item.nombre_administrativo])

    def item_author_name(self, item):
        return item.autor

    def item_author_email(self, obj):
        obj.autor.email

    def item_author_link(self, obj):
        return reverse('apps.sitio.views.usuario_view', args=[obj.autor.id])

    def item_pubdate(self, item):
        return datetime.datetime(item.fecha_publicacion.year, item.fecha_publicacion.month, item.fecha_publicacion.day)

    def item_categories(self, item):
        return [item.nivel.nombre]

    def categories(self):
        return [nivel.nombre for nivel in Nivel.objects.all()]

    def item_guid(self, obj):
        return str(obj.id)
