from django.db import models
from uuid import uuid1

class Libro(models.Model):
    titulo      = models.CharField(max_length=50)
    grupo       = models.SlugField(max_length=50)

class Capitulo(models.Model):
    titulo      = models.CharField(max_length=50)
    libro       = models.ForeignKey(Libro)
    archivo     = models.FileField(upload_to='libro')

class Codigo(models.Model):
    codigo              = models.CharField(max_length=36, default=str(uuid1()))
    usado               = models.BooleanField(default=False)
    fecha_activacion    = models.DateTimeField(blank=True, null=True)
    usuario             = models.ForeignKey('auth.User', blank=True, null=True)
    libro               = models.ForeignKey(Libro)
