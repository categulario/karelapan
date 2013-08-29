from django.db import models
from tinymce.models import HTMLField
from uuid import uuid1

class Libro(models.Model):
    titulo      = models.CharField(max_length=50)
    descripcion = HTMLField()
    portada     = models.ImageField(upload_to='portadas')
    grupo       = models.SlugField(max_length=50)
    costo       = models.DecimalField(max_digits=7, decimal_places=2)
    lectores    = models.ManyToManyField('auth.User', blank=True, null=True, editable=False, related_name='libros')

    def __unicode__(self):
        return self.titulo

class Capitulo(models.Model):
    titulo      = models.CharField(max_length=50)
    libro       = models.ForeignKey(Libro, related_name='capitulos')
    archivo     = models.FileField(upload_to='libro')

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ['id']

default_code = lambda: str(uuid1())

class Codigo(models.Model):
    codigo              = models.CharField(max_length=36, default=default_code)
    usado               = models.BooleanField(default=False, editable=False)
    fecha_activacion    = models.DateTimeField(blank=True, null=True, editable=False)
    usuario             = models.ForeignKey('auth.User', blank=True, null=True, editable=False, related_name='codigos')
    libro               = models.ForeignKey(Libro)

    def __unicode__(self):
        return self.codigo
