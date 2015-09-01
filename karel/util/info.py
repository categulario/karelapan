#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#
#  Copyright 2012 Developingo <a.wonderful.code@gmail.com>
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
#

VERSION = 0.1
BUILD_DATE = 'Jul 21 2012 16:46:12'

cmd_help = """
Uso: karel [--version] [--help] [--future]
            <command> [-k archivo.karel] [-m mundo1.mdo [mundo2.mdo...]]
            [-d directorio/]

Los comandos mas comunes de Karel son:
   run        Corre un programa en Karel en el mundo especificado, o en
              el mundo por defecto si no se especifica mundo.
   check      Verifica la sintaxis de un programa en Karel
   check_all  Verifica la sintaxis de todos los codigos en una carpeta,
              se usa con: -d directorio/
              N: solo rastrea los archivos con extension .txt y .karel
   test       Evalua un codigo Karel dado el codigo y un archivo de
              condiciones de evaluacion.
   contest    Evalua una carpeta con codigos de karel dado un archivo
              de condiciones de evaluacion

La directiva --future activa las palabras 'verdadero', 'falso' y la
instruccion 'sal-de-bucle'.

Escribe 'karel help <comando>' para mayor informacion sobre un comando
particular.
"""

def ayuda(comando):
    """ Proporciona ayuda especifica de un comando en particular """
    comandos = {
        "run": """Corre un programa en Karel.
Para correr Karel en un mundo vacio prueba:
$ karel run -k codigo.karel

Para correr karel en un archivo de mundo prueba:
$ karel run -k codigo.karel -m mundo.nmdo""",
        "check": """Verifica la sintaxis de un programa en Karel""",
        "check_all": """Verifica la sintaxis de todos los codigos dentro
de una carpeta.""",
        "test": """Prueba un programa de Karel en un mundo de prueba,
los mundos de prueba tienen la extension .kec

Para ejecutar un test prueba con:
$ karel test -k codigo.karel -m mundo.nmdo""",
        "contest": """Evalua una carpeta de codigos de Karel dado un
archivo de condiciones de evaluacion.""",
        "testcase": """Consola interactiva para crear casos de evaluación."""
    }
    try:
        return comandos[comando]
    except KeyError:
        return "No existe ayuda para el comando '%s'. O el comando no existe!"%comando

#TODO mejorar la ayuda
