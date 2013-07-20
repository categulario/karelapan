# -*- coding:utf-8 -*-
from django.db import models

class Noticia(models.Model):
    titulo      = models.CharField(max_length=140)
    contenido   = models.TextField()
    autor       = models.ForeignKey('usuarios.Usuario')
    fecha       = models.DateTimeField(auto_now_add=True)
    pegajoso    = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ['-pegajoso', '-fecha']

class Aviso(models.Model):
    contenido   = models.TextField()
    tipo        = models.CharField(max_length=20, choices=(
        ('success', 'Bien (verde)'),
        ('info', 'Información (azul)'),
        ('warning', 'Advertencia (amarillo)'),
        ('error', 'Error (rojo)'),
    ))
    mostrado    = models.BooleanField(default=True)

    def __unicode__(self):
        return self.contenido

class PreguntaFrecuente(models.Model):
    pregunta        = models.CharField(max_length=254)
    respuesta       = models.TextField()
    ordenacion      = models.IntegerField(choices=((i, str(i)) for i in xrange(1, 101)))
    mostrado        = models.BooleanField(default=True)

    def respuesta_full(self):
        return self.respuesta
    respuesta_full.allow_tags = True

    def __unicode__(self):
        return self.pregunta

    class Meta:
        ordering = ['ordenacion']
        verbose_name_plural = 'preguntas frecuentes'
