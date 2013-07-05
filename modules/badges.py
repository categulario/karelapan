# -*- coding:utf-8 -*-
# Funciones varias para el trabajo con la interfaz de karelapan

def badgify(puntaje, total=100):
    if puntaje == '---' or puntaje == -1:
        return '<span class="badge badge-inverse">---</span>'
    if puntaje == total:
        return '<span class="badge badge-success">%d</span>'%puntaje
    if puntaje/float(total) > .66:
        return '<span class="badge badge-info">%d</span>'%puntaje
    if puntaje/float(total) > .33:
        return '<span class="badge badge-warning">%d</span>'%puntaje
    if puntaje/float(total) > 0:
        return '<span class="badge badge-important">%d</span>'%puntaje
    if puntaje == 0:
        return '<span class="badge">0</span>'
