# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from apps.evaluador.models import Envio, Concurso
from django.db.models import Min, Max
from django.utils import timezone
from django.conf import settings
from modules.badges import badgify
import datetime, hashlib

class Grupo(models.Model):
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=240)
    elegible    = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre

class Olimpiada(models.Model):
    anio        = models.IntegerField(default=datetime.date.today().year)
    sede        = models.CharField(max_length=140, blank=True)

    def __unicode__(self):
        return "%d %s"%(self.anio, self.sede)

    class Meta:
        ordering = ['anio']

def default_group():
    return [Grupo.objects.get_or_create(nombre='usuarios', elegible=True)[0]]

def default_omi():
    return Olimpiada.objects.get_or_create(anio=1512)[0]


class Perfil(models.Model):
    usuario             = models.OneToOneField(User)
    nombre              = models.CharField(max_length=120)
    appat               = models.CharField(max_length=120, verbose_name='apellido paterno')
    apmat               = models.CharField(max_length=120, verbose_name='apellido materno')
    estado              = models.CharField(max_length=25, choices=(
        ('extranjero', 'Extranjero'),
        ('aguascalientes', 'Aguascalientes'),
        ('baja_california_norte', 'Baja California Norte'),
        ('baja_california_sur', 'Baja California Sur'),
        ('campeche', 'Campeche'),
        ('chiapas', 'Chiapas'),
        ('chihuahua', 'Chihuahua'),
        ('coahuila', 'Coahuila'),
        ('colima', 'Colima'),
        ('df', 'Distrito Federal'),
        ('durango', 'Durango'),
        ('guanajuato', 'Guanajuato'),
        ('guerrero', 'Guerrero'),
        ('hidalgo', 'Hidalgo'),
        ('jalisco', 'Jalisco'),
        ('mexico', 'Estado de México'),
        ('michoacan', 'Michoacán'),
        ('morelos', 'Morelos'),
        ('nayarit', 'Nayarit'),
        ('nuevo_leon', 'Nuevo León'),
        ('oaxaca', 'Oaxaca'),
        ('puebla', 'Puebla'),
        ('queretaro', 'Querétaro'),
        ('quintana_roo', 'Quintana Roo'),
        ('san_luis_potosi', 'San Luis Potosí'),
        ('sinaloa', 'Sinaloa'),
        ('sonora', 'Sonora'),
        ('tabasco', 'Tabasco'),
        ('tamaulipas', 'Tamaulipas'),
        ('tlaxcala', 'Tlaxcala'),
        ('veracruz', 'Veracruz'),
        ('yucatan', 'Yucatán'),
        ('zacatecas', 'Zacatecas')
    ), default='veracruz')
    sexo                = models.CharField(max_length=1, choices=(
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ), default='M')
    subsistema          = models.CharField(max_length=20, choices=(
        ('PRIMARIAS',)*2,
        ('SECUNDARIAS',)*2,
        ('DGETI',)*2,
        ('CECYTEV',)*2,
        ('DGETA',)*2,
        ('DGB',)*2,
        ('COBAEV',)*2,
        ('CONALEP',)*2,
        ('TEBAEV',)*2,
        ('PARTICULAR',)*2,
        ('OTROS',)*2
    ), default='OTROS')
    nivel_estudios      = models.CharField(max_length=20, choices=(
        ('kinder', 'Kinder'),
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('bachillerato', 'Bachillerato'),
        ('profesional', 'Profesional')
    ), default='secundaria')
    grado_actual        = models.CharField(max_length=20, choices=(
        ('primaria', 'Primaria'),
        ('1 secundaria', '1º año secundaria'),
        ('2 secundaria', '2º año secundaria'),
        ('3 secundaria', '3º año secundaria'),
        ('1 bachillerato', '1º semestre bachillerato'),
        ('2 bachillerato', '2º semestre bachillerato'),
        ('3 bachillerato', '3º semestre bachillerato'),
        ('4 bachillerato', '4º semestre bachillerato'),
        ('5 bachillerato', '5º semestre bachillerato'),
        ('6 bachillerato', '6º semestre bachillerato'),
        ('otro', 'otro')
    ), default='2 bachillerato')
    fecha_nacimiento    = models.DateField(null=True)
    asesor              = models.ForeignKey('usuarios.Usuario', null=True, blank=True, related_name='asesorados')
    nombre_escuela      = models.CharField(max_length='140', blank=True)
    problemas_resueltos = models.IntegerField(default=0)
    puntaje             = models.IntegerField(default=0)
    descripcion         = models.TextField()
    grupos              = models.ManyToManyField(Grupo, related_name='perfiles')
    ultima_omi          = models.ForeignKey(Olimpiada, default=default_omi, related_name='+')
    confirm_token       = models.CharField(max_length=36, blank=True, null=True, editable=False)
    nombre_completo     = models.CharField(max_length=200, blank=True, null=True)
    inscripciones       = models.ManyToManyField(Olimpiada, null=True, blank=True, related_name='inscritos')

    def es_olimpico(self):
        olimpiada_actual = Olimpiada.objects.get_or_create(anio=settings.OLIMPIADA_ACTUAL)[0]
        return olimpiada_actual in self.inscripciones.all()

    def get_full_name(self):
        return "%s %s %s"%(self.nombre, self.appat, self.apmat)

    def correo(self):
        return self.usuario.email

    def lista_grupos(self):
        return ', '.join([str(g) for g in self.grupos.all()])

    def __unicode__(self):
        return self.get_full_name()

    def gravatar(self):
        return 'http://www.gravatar.com/avatar/'+hashlib.md5(str(self.usuario.email).lower()).hexdigest()+'?s=200&r=g&d=monsterid'

    def gravatar_pequenio(self):
        return 'http://www.gravatar.com/avatar/'+hashlib.md5(str(self.usuario.email).lower()).hexdigest()+'?s=25&r=g&d=monsterid'

    def save(self):
        self.nombre_completo = "%s %s %s"%(self.nombre, self.appat, self.apmat)
        super(Perfil, self).save()
        self.grupos.add(Grupo.objects.get_or_create(nombre='usuarios')[0])
        super(Perfil, self).save()

    class Meta:
        verbose_name_plural = 'perfiles'

class Usuario(User):
    class Meta:
        proxy = True
        ordering = ('perfil__nombre', 'perfil__appat', 'perfil__apmat')

    def gravatar(self):
        return 'http://www.gravatar.com/avatar/'+hashlib.md5(str(self.email).lower()).hexdigest()+'?s=200&r=g&d=monsterid'

    def gravatar_pequenio(self):
        return 'http://www.gravatar.com/avatar/'+hashlib.md5(str(self.email).lower()).hexdigest()+'?s=25&r=g&d=monsterid'

    def lista_problemas_intentados(self):
        problemas_resueltos = self.lista_problemas_resueltos()
        lista_problemas = []
        for envio in Envio.objects.filter(puntaje__lt=100, usuario=self, concurso=None):
            if envio.problema not in lista_problemas and envio.problema not in problemas_resueltos:
                problema = envio.problema
                problema.mejor_puntaje_usuario = badgify(Envio.objects.filter(usuario=self, problema=problema, concurso=None).aggregate(Max('puntaje'))['puntaje__max'])
                lista_problemas.append(problema)
        return lista_problemas

    def lista_problemas_resueltos(self):
        lista_problemas = []
        for envio in Envio.objects.filter(puntaje=100, usuario=self, concurso=None):
            if envio.problema not in lista_problemas:
                problema = envio.problema
                problema.mejor_tiempo_usuario = Envio.objects.filter(usuario=self, problema=problema, resultado='OK', concurso=None).aggregate(Min('tiempo_ejecucion'))['tiempo_ejecucion__min']
                lista_problemas.append(problema)
        return lista_problemas

    def mejor_puntaje(self, problema, concurso=None):
        envios = Envio.objects.filter(usuario=self, problema=problema, concurso=concurso)
        if envios:
            return envios.aggregate(Max('puntaje'))['puntaje__max']
        else:
            return '---'

    def primer_puntaje(self, problema, concurso=None):
        envios = Envio.objects.filter(usuario=self, problema=problema, concurso=concurso)
        if envios:
            return envios.order_by('hora')[0].puntaje
        else:
            return '---'

    def intentos(self, problema, concurso=None):
        return Envio.objects.filter(usuario=self, problema=problema, concurso=concurso).count()

    def mejor_tiempo(self, problema, concurso=None):
        envios = Envio.objects.filter(usuario=self, problema=problema, concurso=concurso, puntaje=100)
        if envios:
            return envios.aggregate(Min('tiempo_ejecucion'))['tiempo_ejecucion__min']
        else:
            return '---'

    def usuarios_resuelto(self, problema):
        lista_usuarios = []
        for envio in Envio.objects.filter(puntaje=100, problema=problema, concurso=None).order_by('usuario__perfil__puntaje'):
            if envio.usuario not in lista_usuarios:
                lista_usuarios.append(Usuario.objects.get(pk=envio.usuario.id))
        return lista_usuarios

    def usuarios_intentado(self, problema):
        usuarios_resueltos = self.usuarios_resuelto(problema)
        lista_usuarios = []
        for envio in Envio.objects.filter(puntaje__lt=100, problema=problema, concurso=None):
            if Usuario.objects.get(pk=envio.usuario.id) not in lista_usuarios and Usuario.objects.get(pk=envio.usuario.id) not in usuarios_resueltos:
                lista_usuarios.append(Usuario.objects.get(pk=envio.usuario.id))
        return lista_usuarios

    def concursos_activos(self):
        return Concurso.objects.filter(
            grupos__perfiles=self.perfil,
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now(),
            activo=True
        )

    def concursos_activos_y_futuros(self):
        concursos = Concurso.objects.filter(
            grupos__perfiles=self.perfil,
            fecha_fin__gte=timezone.now(),
            activo=True
        )
        lista = []
        for concurso in concursos:
            if concurso.fecha_inicio <= timezone.now():
                concurso.en_curso = True
            else:
                concurso.en_curso = False
            lista.append(concurso)
        return lista

    def participa_en_concurso(self):
        return self.concursos_activos().count() > 0

    def puede_hacer_consulta(self, concurso):
        """determina si el usuario puede hacer una consulta en un examen
        en el que participa"""
        return concurso in self.concursos_activos() and concurso.fecha_inicio < timezone.now() and timezone.now() < (concurso.fecha_inicio + datetime.timedelta(minutes=concurso.duracion_preguntas))

    def lista_grupos(self):
        return ', '.join([str(g) for g in self.perfil.grupos.all()])

    def get_full_name(self):
        return "%s %s %s"%(self.perfil.nombre, self.perfil.appat, self.perfil.apmat)

    def get_short_name(self):
        return self.perfil.nombre

    def __unicode__(self):
        return "%s %s %s"%(self.perfil.nombre, self.perfil.appat, self.perfil.apmat)

