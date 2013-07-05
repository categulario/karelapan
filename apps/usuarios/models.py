# -*- coding:utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from apps.evaluador.models import Envio
from django.db.models import Min, Max
import datetime

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
    try:
        return [Grupo.objects.get(nombre='usuarios')]
    except ObjectDoesNotExist:
        g = Grupo(nombre='usuarios', descripcion='Usuarios generales del sistema', elegible=True)
        g.save()
        return [g]

def default_omi():
    try:
        return Olimpiada.objects.get(anio=datetime.date.today().year)
    except ObjectDoesNotExist:
        o = Olimpiada(anio=datetime.date.today().year)
        o.save()
        return o

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None):
        if not correo or type(correo) != str:
            raise ValueError('Es necesario el correo')

        user = self.model(correo=correo)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password):
        user = self.create_user(correo, password=password,)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    correo              = models.EmailField(max_length=254, unique=True, db_index=True)
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
    asesor              = models.ForeignKey('self', null=True, blank=True)
    nombre_escuela      = models.CharField(max_length='140', blank=True)
    problemas_resueltos = models.IntegerField(default=0)
    puntaje             = models.IntegerField(default=0)
    descripcion         = models.TextField()
    grupo               = models.ManyToManyField(Grupo, default=default_group)
    ultima_omi          = models.ForeignKey(Olimpiada, default=default_omi)

    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)
    fecha_registro      = models.DateTimeField(auto_now_add=True)
    problemas           = models.ManyToManyField('evaluador.Problema', through='evaluador.Envio', blank=True, editable=False)

    USERNAME_FIELD = 'correo'
    objects = UsuarioManager()

    def lista_problemas_intentados(self):
        problemas_resueltos = self.lista_problemas_resueltos()
        lista_problemas = []
        for envio in Envio.objects.filter(puntaje__lt=100, usuario=self, concurso=None):
            if envio.problema not in lista_problemas and envio.problema not in problemas_resueltos:
                problema = envio.problema
                problema.mejor_puntaje_usuario = Envio.objects.filter(usuario=self, problema=problema, concurso=None).aggregate(Max('puntaje'))['puntaje__max']
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

    def lista_grupos(self):
        return ','.join([str(g) for g in self.grupo.all()])

    def get_full_name(self):
        return "%s %s %s"%(self.nombre, self.appat, self.apmat)

    def get_short_name(self):
        return self.nombre

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return "%s %s %s"%(self.nombre, self.appat, self.apmat)

    class Meta:
        ordering = ('nombre', 'appat', 'apmat')
