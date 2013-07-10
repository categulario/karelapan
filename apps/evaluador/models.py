# -*- coding:utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
import json
import os

def valida_mundos(str_mundo):
    """valida que 'str_mundo' sea un documento JSON que representa un
    mundo válido de karel"""
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
    """Obtiene el nombre que tendrá el archivo de un set de casos de
    evaluación"""
    return os.path.join('casos', problema.nombre_administrativo+'.nkec')

def valida_json(cadena):
    """identifica si la cadena es json"""
    try:
        json.loads(cadena)
    except:
        raise ValidationError('No es un json valido')

class Nivel(models.Model):
    """Los problemas del evaluador están agrupados en estos niveles para
    su mejor desarrollo con los usuarios"""
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    nivel       = models.IntegerField()

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'niveles'
        ordering            = ['nivel']


class Problema(models.Model):
    """Un problema del evaluador o de un concurso para resolverse con
    karel"""
    nombre                  = models.CharField(max_length=140, unique=True)
    nombre_administrativo   = models.CharField(max_length=140, unique=True)
    descripcion             = models.TextField()
    problema                = models.TextField()
    agradecimiento          = models.TextField(blank=True)
    veces_resuelto          = models.IntegerField(default=0)
    veces_intentado         = models.IntegerField(default=0)
    mejor_tiempo            = models.IntegerField(default=-1)
    mejor_puntaje           = models.IntegerField(default=-1)
    autor                   = models.ForeignKey('usuarios.Usuario')
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
    """Cada problema de karel tiene consideraciones que limitan el mundo
    """
    problema    = models.ForeignKey(Problema)
    texto       = models.CharField(max_length=254)

    def __unicode__(self):
        return self.texto

    class Meta:
        verbose_name_plural = 'consideraciones'


class Concurso(models.Model):
    """Los usuarios pueden concursar y sacar puntajes independientes en
    este tipo de concursos"""
    fecha_inicio        = models.DateTimeField()
    fecha_fin           = models.DateTimeField()
    nombre              = models.CharField(max_length=140)
    descripcion         = models.TextField()
    activo              = models.BooleanField(default=True)
    autor               = models.ForeignKey('usuarios.Usuario')
    problemas           = models.ManyToManyField(Problema)
    grupos              = models.ManyToManyField('usuarios.Grupo')
    duracion_preguntas  = models.IntegerField(default=90, help_text="La duración en minutos del periodo en que pueden hacer preguntas los concursantes a partir del inicio del concurso")

    def __unicode__(self):
        return self.nombre

    def lista_grupos(self):
        return ', '.join([str(g) for g in self.grupos.all()])

    class Meta:
        permissions = (
            ("puede_ver_ranking", "Puede ver ranking"),
        )
        ordering    = ['-fecha_inicio']


class Participacion(models.Model):
    """Maneja la participación de un usuario en un concurso"""
    usuario     = models.ForeignKey('usuarios.Usuario')
    concurso    = models.ForeignKey(Concurso)
    puntaje     = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'participaciones'
        unique_together = ("usuario", "concurso")


class Envio(models.Model):
    """Describe un envío que se va a la cola de evaluación"""
    usuario             = models.ForeignKey('usuarios.Usuario')
    problema            = models.ForeignKey(Problema)
    hora                = models.DateTimeField(auto_now_add=True)
    estatus             = models.CharField(max_length=1, choices=(
        ('E', 'Evaluado'),
        ('P', 'Pendiente de evaluacion'),
        ('S', 'En evaluación')
    ), default='P')
    puntaje             = models.IntegerField(default=0)
    codigo              = models.TextField(blank=True, null=True)
    codigo_archivo      = models.FilePathField(path='/home/abraham/Desarrollo/django/KarelapanDjango/codigos')
    tiempo_ejecucion    = models.IntegerField(default=0)
    resultado           = models.CharField(max_length=17, choices=(
        ('OK', 'Ok'),
        ('ERROR_COMPILACION', 'Error de compilación'),
        ('CASOS_INCOMPLETOS', 'Casos incompletos')
    ), default='OK')
    mensaje             = models.CharField(max_length=250, blank=True)
    concurso            = models.ForeignKey(Concurso, null=True, blank=True)
    ip                  = models.IPAddressField(blank=True, null=True, default='0.0.0.0')
    casos               = models.TextField(validators=[valida_json], blank=True)

    def lee_casos(self):
        class Caso:
            def __init__(self, puntos_obtenidos, mensaje, puntos_valor, terminacion):
                self.puntos_obtenidos = puntos_obtenidos
                self.mensaje = mensaje
                self.puntos_valor = puntos_valor
                self.terminacion = terminacion
        jason = json.loads(self.casos)
        arr_casos = []
        for casito in jason:
            arr_casos.append(Caso(casito['obtenidos'], casito['mensaje'], casito['puntos'], casito['terminacion']))
        return arr_casos

    class Meta:
        ordering    = ['-hora']


class Consulta(models.Model):
    """Un mensaje de aclaración para el usuario en el concurso que esté
    participando"""
    concurso    = models.ForeignKey(Concurso)
    problema    = models.ForeignKey(Problema)
    usuario     = models.ForeignKey('usuarios.Usuario')
    mensaje     = models.CharField(max_length=140)
    respuesta   = models.TextField()
    leido       = models.BooleanField(default=False)
    hora        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering    = ['hora']

    def __unicode__(self):
        return self.mensaje
