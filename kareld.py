#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#
#  Copyright 2012 Abraham Toriz Cruz <a.wonderful.code@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Demonio evaluador de Karel
import psycopg2, json
from psycopg2.extras import DictCursor
from karel.kgrammar import kgrammar
from karel.kworld import kworld
from karel.krunner import krunner
from karel.kutil import KarelException
from karelapan import settings
from time import time, sleep

connection = psycopg2.connect("dbname=%s user=%s password=%s"%(settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD']))
cursor = connection.cursor(cursor_factory=DictCursor)

while True:
    cursor.execute("SELECT * FROM evaluador_envio WHERE estatus='P' ORDER BY hora ASC")
    envio = cursor.fetchone() #El envío a calificar
    if envio is not None:
        cursor.execute("UPDATE evaluador_envio SET estatus='S' WHERE id='%d'"%envio['id'])
        connection.commit()#Nos aseguramos de marcar este envio y evitar que otra llamada del evaluador lo revise
        cursor.execute("SELECT * FROM evaluador_problema WHERE id='%d'"%envio['problema_id'])
        problema = cursor.fetchone() #El problema
        resultado = { #Almacena el resultado de esta ejecución
            "resultado": "OK", #puede ser ERROR_COMPILACION Ó CASOS_INCOMPLETOS
            "mensaje": "Ejecución terminada",
            "casos": [],
            "puntaje": 0,
            "total": 0,
            "efectividad": 0.0,
            "tiempo_ejecucion": 0
        }
        archivomundo = settings.MEDIA_ROOT+'/'+problema['casos_de_evaluacion']
        f = file(archivomundo)
        kec = json.load(f) #Tenemos el archivo de condiciones de evaluacion cargado.
        arch = envio['codigo_archivo'] #Programa a evaluar
        grammar = kgrammar(flujo=open(arch), archivo=arch, strict=True,futuro=problema['futuro'], strong_logic=problema['logica_fuerte'])
        try:
            grammar.verificar_sintaxis() #Pedimos que genere el arbol de instrucciones
            grammar.expandir_arbol()
        except KarelException, ke:
            resultado['mensaje'] = "El archivo tiene errores: %s cerca de la linea %d"%(ke[0], grammar.obtener_linea_error())
            resultado['resultado'] = "ERROR_COMPILACION"
        else:
            t_inicio = time()
            puntaje = 0
            num_caso = 0
            suma_puntos = 0
            for caso in kec['casos']:
                num_caso += 1
                mun = kworld(filas=caso['mundo']['dimensiones']['filas'], columnas=caso['mundo']['dimensiones']['columnas'], karel_pos=tuple(caso['mundo']['karel']['posicion']), orientacion=caso['mundo']['karel']['orientacion'], mochila=caso['mundo']['karel']['mochila'])
                mun.carga_casillas(caso['mundo']['casillas'])

                limite_recursion = problema['limite_recursion']
                limite_iteracion = problema['limite_iteracion']
                limite_ejecucion = problema['limite_ejecucion']

                runner = krunner(
                    grammar.ejecutable,
                    mundo=mun,
                    limite_recursion=limite_recursion,
                    limite_iteracion=limite_iteracion,
                    limite_ejecucion=limite_ejecucion
                )
                runner.run()
                all_ok = True
                if runner.estado == 'OK':
                    if caso['resultado'].has_key('karel'):
                        #Debemos buscar la posicion de karel o su mochila
                        if caso['resultado']['karel'].has_key('posicion'):
                            #verificamos la posicion
                            if tuple(caso['resultado']['karel']['posicion']) != runner.mundo.mundo['karel']['posicion']:
                                all_ok = False
                                runner.mensaje = 'La posicion de Karel es incorrecta'
                        if caso['resultado']['karel'].has_key('orientacion'):
                            #verificamos la posicion
                            if caso['resultado']['karel']['orientacion'] != runner.mundo.mundo['karel']['orientacion']:
                                all_ok = False
                                runner.mensaje = 'La orientacion de Karel es incorrecta'
                        if caso['resultado']['karel'].has_key('mochila'):
                            #verificamos la posicion
                            if caso['resultado']['karel']['mochila'] != runner.mundo.mundo['karel']['mochila']:
                                all_ok = False
                                runner.mensaje = 'La cantidad de zumbadores en la mochila de Karel es incorrecta'
                    if caso['resultado'].has_key('casillas'):
                        for casilla in caso['resultado']['casillas']:
                            fila, columna = casilla['fila'], casilla['columna']
                            if runner.mundo.mundo['casillas'].has_key((fila, columna)):
                                if runner.mundo.mundo['casillas'][(fila, columna)]['zumbadores'] != casilla['zumbadores']:
                                    all_ok = False
                                    runner.mensaje = 'La cantidad de zumbadores en el mundo es incorrecta!'
                                    break
                            elif casilla['zumbadores'] != 0:
                                all_ok = False
                                runner.mensaje = 'La cantidad de zumbadores en el mundo es incorrecta!'
                                break
                    if all_ok:
                        puntaje += int(caso['puntaje'])
                    else:
                        runner.estado = 'ERROR'
                        resultado['resultado'] = "CASOS_INCOMPLETOS"
                        resultado['mensaje'] = "Tu codigo no funciona en todos los casos"
                else:
                    resultado['resultado'] = "CASOS_INCOMPLETOS"
                    resultado['mensaje'] = 'Tu codigo no funciona en todos los casos'
                suma_puntos += int(caso['puntaje'])
                resultado['casos'].append({
                    "terminacion": runner.estado,
                    "mensaje": runner.mensaje,
                    "puntos": caso['puntaje'],
                    "obtenidos": [0, caso['puntaje']][all_ok]
                })
            t_fin = time()
            resultado['puntaje'] = puntaje
            resultado['total'] = suma_puntos
            resultado['efectividad'] = puntaje/float(suma_puntos)
            resultado['tiempo_ejecucion'] = int((t_fin-t_inicio)*1000)
        #TODO hacer las cosas respectivas con los valores obtenidos
        if resultado['resultado'] == 'OK': #La evaluación es buena, el usuario incremeta problemas resuelto y el problema veces resuelto.
            cursor.execute('UPDATE usuarios_usuario SET problemas_resueltos=problemas_resueltos+1 WHERE id=%s', (envio['usuario_id'], ))
            connection.commit()
            cursor.execute('UPDATE evaluador_problema SET veces_resuelto=veces_resuelto+1 WHERE id=%s', (envio['problema_id'], ))
            connection.commit()
        cursor.execute("UPDATE evaluador_envio SET estatus='E', puntaje=%s, tiempo_ejecucion=%s, resultado=%s, mensaje=%s, casos=%s WHERE id=%s", (
            resultado['puntaje'],
            resultado['tiempo_ejecucion'],
            resultado['resultado'],
            resultado['mensaje'],
            json.dumps(resultado['casos']),
            envio['id']
        ))
        connection.commit()
    sleep(2)
cursor.close()
connection.close()
