# -*- coding:utf-8 -*-
from django.db import models
from apps.usuarios.models import Usuario, Grupo
from django.core.exceptions import ValidationError
import pymongo
import json
import os

def valida_dimensiones(cadena):
    """Valida una cadena de dimensiones para usarse como dimensiones de
    renderizado de mundos"""
    try:
        d = [int(i) for i in cadena.split(',')]
        if len(d)!=4:
            raise ValueError('Hay menos de cuatro valores aquí')
        for i in d:
            if i<1 or i>100:
                raise ValueError('Uno de los valores está fuera de rango')
    except ValueError:
        raise ValidationError('No pude convertir todos los números')

def valida_mundos(str_mundo):
    try:
        mundo = json.loads(str_mundo)
    except ValueError:
        raise ValidationError('No pude leer este mundo como json')
    else:
        if 'karel' in mundo and 'casillas' in mundo and 'dimensiones' in mundo:
            if 'posicion' in mundo['karel'] and 'orientacion' in mundo['karel'] and 'mochila' in mundo['karel']:
                if type(mundo['karel']['posicion']) == list and mundo['karel']['orientacion'] in ['norte', 'sur', 'este', 'oeste'] and type(mundo['karel']['mochila'])==int and type(mundo['casillas']) == list:
                    if 0<mundo['dimensiones']['filas']<=100 and 0<mundo['dimensiones']['columnas']<=100 and mundo['karel']['mochila']>=-1:
                        bueno = True
                        for casilla in mundo['casillas']:
                            if 'fila' in casilla and 'columna' in casilla and 'paredes' in casilla and 'zumbadores' in casilla:
                                if type(casilla['fila'])==int and type(casilla['columna'])==int and type(casilla['zumbadores'])==int and type(casilla['paredes']) == list:
                                    if 0<casilla['fila']<=100 and 0<casilla['columna']<=100 and casilla['zumbadores']>=-1:
                                        bparedes = True
                                        for pared in casilla['paredes']:
                                            if pared not in ['norte', 'sur', 'este', 'oeste']:
                                                bparedes = False
                                                break
                                        if not bparedes:
                                            raise ValidationError('Valor inválido para pared')
                                    else:
                                        bueno = False
                                        break
                                else:
                                    bueno = False
                                    break
                            else:
                                bueno = False
                                break
                        if not bueno:
                            raise ValidationError('Error en una de las casillas')
                    else:
                        raise ValidationError('Las dimensiones sobrepasan lo permitido')
                else:
                    raise ValidationError('El tipo de dato de una llave no coincide')
            else:
                raise ValidationError('Este mundo no tiene una de las llaves posicion, orientación o mochila')
        else:
            raise ValidationError('Este mundo no contiene las llaves principales de karel, mundo y casillas')

def url_casos_evaluacion(problema, nombre_original_archivo):
    return os.path.join('casos', problema.nombre_administrativo+'.nkec')

class Nivel(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    nivel       = models.IntegerField()

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'niveles'
        ordering            = ['nivel']


class Problema(models.Model):
    nombre                  = models.CharField(max_length=140, unique=True)
    nombre_administrativo   = models.CharField(max_length=140, unique=True)
    descripcion             = models.TextField()
    problema                = models.TextField()
    agradecimiento          = models.TextField()
    veces_resuelto          = models.IntegerField(default=0)
    veces_intentado         = models.IntegerField(default=0)
    mejor_tiempo            = models.IntegerField(default=-1)
    mejor_puntaje           = models.IntegerField(default=-1)
    autor                   = models.ForeignKey(Usuario)
    fecha_publicacion       = models.DateField(auto_now_add=True)
    nivel                   = models.ForeignKey(Nivel)
    publico                 = models.BooleanField(default=True)
    futuro                  = models.BooleanField(default=False)
    logica_fuerte           = models.BooleanField(default=False)
    limite_recursion        = models.IntegerField(default=65000)
    limite_iteracion        = models.IntegerField(default=65000)
    limite_ejecucion        = models.IntegerField(default=200000)
    mundo                   = models.TextField(validators=[valida_mundos])
    mundo_resuelto          = models.TextField(validators=[valida_mundos])
    dimensiones             = models.CharField(max_length=15, validators=[valida_dimensiones])
    casos_de_evaluacion     = models.FileField(upload_to=url_casos_evaluacion)

    def __unicode__(self):
        return self.nombre

    def mejor_puntaje_usuario(self, id_usuario):
        connection = pymongo.Connection()
        db = connection['envios']
        collection = db['intentos']
        resultado = collection.find_one({'problema':self.id, 'usuario':id_usuario}).sort('puntaje', direction=pymongo.DESCENDING)
        if resultado == None:
            return -1
        else:
            return resultado['puntaje']


class Consideracion(models.Model):
    problema    = models.ForeignKey(Problema)
    texto       = models.CharField(max_length=254)

    def __unicode__(self):
        return self.texto

    class Meta:
        verbose_name_plural = 'consideraciones'


class Concurso(models.Model):
    fecha_inicio    = models.DateTimeField()
    fecha_fin       = models.DateTimeField()
    nombre          = models.CharField(max_length=140)
    descripcion     = models.TextField()
    activo          = models.BooleanField(default=True)
    autor           = models.ForeignKey(Usuario)
    problemas       = models.ManyToManyField(Problema)
    grupos          = models.ManyToManyField(Grupo)

    def __unicode__(self):
        return self.nombre

    class Meta:
        permissions = (
            ("puede_ver_ranking", "Puede ver ranking"),
        )

class Participacion(models.Model):
    usuario     = models.ForeignKey(Usuario)
    concurso    = models.ForeignKey(Concurso)
    puntaje     = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'participaciones'
        unique_together = ("usuario", "concurso")
