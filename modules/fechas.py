# -*- coding:utf-8 -*-
from django.utils import timezone

def diferencia_str(fecha_evento):
    """Calcula y crea un string con el tiempo restante para este evento
    """
    diferencia = fecha_evento - timezone.now()
    quedan_dias    = ['', "%d días"%diferencia.days][diferencia.days!=0]
    horas = diferencia.seconds/3600
    quedan_horas   = ['', " %d horas"%horas][horas!=0]
    minutos = (diferencia.seconds/60)%60
    quedan_minutos = ['', " %d minutos"%minutos][minutos!=0]
    segundos = diferencia.seconds%60
    quedan_segundos = ['', ' %d segundos'%segundos][segundos!=0]
    return "%s %s %s %s"%(quedan_dias, quedan_horas, quedan_minutos, quedan_segundos)
