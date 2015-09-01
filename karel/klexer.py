# -*- coding: utf-8 -*-
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
import sys
from kutil import KarelException, ktoken

"""
El analizador léxico de Karel completamente reescrito por mi para la
sintaxis pascal
"""

class klexer(object):
    """analizador léxico de karel"""
    ESTADO_ESPACIO = ' '
    ESTADO_PALABRA = 'a'
    ESTADO_COMENTARIO = '#'
    ESTADO_NUMERO = '0'
    ESTADO_SIMBOLO = '+'
    def __init__(self, archivo=sys.stdin, nombre_archivo='', debug=False):
        """Se construye el analizador con el nombre del archivo"""
        self.archivo = archivo
        self.nombre_archivo = nombre_archivo

        self.numeros = "0123456789"
        self.palabras = "abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        self.simbolos = "(){}*/;,|&!#" #Simbolos permitidos para esta sintaxis
        self.espacios = " \n\r\t"

        self.caracteres = self.numeros+self.palabras+self.simbolos+self.espacios

        self.ultimo_caracter = ''
        self.caracter_actual = ''
        self.abrir_comentario = '' #Indica cómo fue abierto un comentario

        self.pila_tokens = [] #Pila de tokens por si me lo devuelven

        self.linea = 1 #El número de linea
        self.columna = 0#El número de columna
        self.es_primer_token = True #Registra si se trata del primer token de la linea
        self.token = ''
        self.estado = self.ESTADO_ESPACIO

        self.sintaxis = 'pascal' #para la gestion de los comentarios
        self.lonely_chars = [';', '{', '}', '!', ')', '#']

        self.debug = debug
        self.caracter_actual = self.lee_caracter()
        if self.debug:
            print "leyendo archivo '%s'"%self.nombre_archivo

    def establecer_sintaxis(self, sintaxis):
        """Establece la sintaxis para este análisis"""
        if sintaxis == 'java':
            self.lonely_chars += ['(', ')']
        if sintaxis == 'ruby':
            self.lonely_chars.remove('#')
        self.sintaxis = sintaxis

    def lee_caracter(self):
        """Lee un caracter de la fuente o devuelve uno de la pila si no
        está vacía"""
        self.ultimo_caracter = self.caracter_actual
        return self.archivo.read(1)

    def get_token(self):
        """Obtiene el siguiente token. Si la pila tiene tokens le quita
        uno, si no, obtiene el siguiente token del archivo"""
        if len(self.pila_tokens)>0:
            return self.pila_tokens.pop()
        else:
            return self.lee_token()

    def push_token(self, token):
        """Empuja un token en la pila"""
        self.pila_tokens.append(token)

    def cambio_de_linea(self):
        self.linea += 1
        self.columna = 0
        self.es_primer_token = True

    def lee_token(self):
        """Lee un token del archivo"""
        while True:
            self.columna += 1
            if not self.caracter_actual:
                break
            if self.estado == self.ESTADO_COMENTARIO:
                if self.debug:
                    print "Encontré", repr(self.caracter_actual), "en estado comentario"
                if self.caracter_actual in self.simbolos: #Lo que puede pasar es que sea basura o termine el comentario
                    if self.caracter_actual == ')' and self.abrir_comentario == '(*' and self.ultimo_caracter == '*':
                        self.estado = self.ESTADO_ESPACIO
                    if self.caracter_actual == '}' and self.abrir_comentario == '{':
                        self.estado = self.ESTADO_ESPACIO
                    if self.caracter_actual == '/' and self.abrir_comentario == '/*' and self.ultimo_caracter == '*':
                        self.estado = self.ESTADO_ESPACIO
                if self.caracter_actual == '\n': #LINEA
                    self.cambio_de_linea()
            elif self.estado == self.ESTADO_ESPACIO:
                if self.debug:
                    print "Encontré", repr(self.caracter_actual), "en estado espacio"
                if self.caracter_actual not in self.caracteres:
                    raise KarelException("Caracter desconocido en la linea %d columna %d"%(self.linea, self.columna))
                if self.caracter_actual in self.numeros:
                    self.token += self.caracter_actual
                    self.estado = self.ESTADO_NUMERO
                elif self.caracter_actual in self.palabras:
                    self.token += self.caracter_actual
                    self.estado = self.ESTADO_PALABRA
                elif self.caracter_actual in self.simbolos:
                    self.estado = self.ESTADO_SIMBOLO
                    continue
                elif self.caracter_actual == '\n': #LINEA
                    self.cambio_de_linea()
            elif self.estado == self.ESTADO_NUMERO:
                if self.debug:
                    print "Encontré", repr(self.caracter_actual), "en estado número"
                if self.caracter_actual not in self.caracteres:
                    raise KarelException("Caracter desconocido en la linea %d columna %d"%(self.linea, self.columna))
                if self.caracter_actual in self.numeros:
                    self.token += self.caracter_actual
                elif self.caracter_actual in self.palabras: #Encontramos una letra en el estado numero, incorrecto
                    raise KarelException("Este token no parece valido, linea %d columna %d"%(self.linea, self.columna))
                elif self.caracter_actual in self.simbolos:
                    self.estado = self.ESTADO_SIMBOLO
                    break
                elif self.caracter_actual in self.espacios:
                    self.estado = self.ESTADO_ESPACIO
                    break #Terminamos este token
            elif self.estado == self.ESTADO_PALABRA:
                if self.debug:
                    print "Encontré", repr(self.caracter_actual), "en estado palabra"
                if self.caracter_actual not in self.caracteres:
                    raise KarelException("Caracter desconocido en la linea %d columna %d"%(self.linea, self.columna))
                if self.caracter_actual in self.palabras+self.numeros:
                    self.token += self.caracter_actual
                elif self.caracter_actual in self.simbolos:
                    self.estado = self.ESTADO_SIMBOLO
                    break
                elif self.caracter_actual in self.espacios:
                    self.estado = self.ESTADO_ESPACIO
                    break #Terminamos este token
            elif self.estado == self.ESTADO_SIMBOLO:
                if self.debug:
                    print "Encontré", repr(self.caracter_actual), "en estado símbolo"
                if self.caracter_actual not in self.caracteres:
                    raise KarelException("Caracter desconocido en la linea %d columna %d"%(self.linea, self.columna))
                if self.caracter_actual == '{' and self.sintaxis=='pascal':
                    self.abrir_comentario = '{'
                    self.estado = self.ESTADO_COMENTARIO
                    if self.token:
                        break
                elif self.caracter_actual == '#':
                    self.estado = self.ESTADO_ESPACIO
                    self.archivo.readline() #LINEA
                    self.cambio_de_linea()
                    if self.token:
                        break
                elif self.caracter_actual in self.numeros:
                    self.estado = self.ESTADO_NUMERO
                    if self.token:
                        break
                elif self.caracter_actual in self.palabras:
                    self.estado = self.ESTADO_PALABRA
                    if self.token:
                        break
                elif self.caracter_actual in self.simbolos: #Encontramos un símbolo en estado símbolo
                    if self.caracter_actual == '/' and self.ultimo_caracter == '/':
                        self.archivo.readline() #LINEA
                        self.cambio_de_linea()
                        self.estado = self.ESTADO_ESPACIO
                        if self.token.endswith('/'):
                            self.token = self.token[:-1]
                        if self.token:
                            self.caracter_actual = self.lee_caracter()
                            break
                    elif self.caracter_actual == '*' and self.ultimo_caracter == '/' and self.sintaxis == 'java':
                        self.estado = self.ESTADO_COMENTARIO
                        self.abrir_comentario = '/*'
                        if self.token.endswith('/'):
                            self.token = self.token[:-1]
                        if self.token:
                            self.caracter_actual = self.lee_caracter()
                            break
                    elif self.caracter_actual == '*' and self.ultimo_caracter == '(' and self.sintaxis == 'pascal':
                        self.estado = self.ESTADO_COMENTARIO
                        self.abrir_comentario = '(*'
                        if self.token.endswith('('):
                            self.token = self.token[:-1]
                        if self.token:
                            self.caracter_actual = self.lee_caracter()
                            break
                    elif self.caracter_actual in self.lonely_chars: #Caracteres que viven solos
                        self.estado = self.ESTADO_ESPACIO
                        if self.token:
                            break
                        self.token += self.caracter_actual
                        self.caracter_actual = self.lee_caracter()
                        break
                    else:
                        self.token += self.caracter_actual
                elif self.caracter_actual in self.espacios:
                    self.estado = self.ESTADO_ESPACIO
                    if self.token:
                        break
                else:
                    raise KarelException("Caracter desconocido en la linea %d columna %d"%(self.linea, self.columna))
            self.caracter_actual = self.lee_caracter()
        token = self.token
        self.token = ''
        obj_token = ktoken(token, self.es_primer_token)
        self.es_primer_token = False
        return obj_token

    def __iter__(self):
        return self

    def next(self):
        """Devuelve un token de la pila si no está vacía o devuelve el
        siguiente token del archivo, esta función sirve al iterador de
        tokens"""
        token = self.get_token()
        if token == '':
            raise StopIteration
        return token


if __name__ == '__main__':
    debug=0
    if '-d' in sys.argv:
        debug=1
    if len(sys.argv)>1 and sys.argv[1] != '-d':
        lexer = klexer(open(sys.argv[1]), sys.argv[1], debug=debug)
    else:
        lexer = klexer(debug=debug)
    i=0
    for token in lexer:
        print "Token:", repr(token), "\t\tLine:", lexer.linea, "\t\tCol:", lexer.columna, "\t\tPrimer:", token.es_primer_token
        i += 1
    print lexer.sintaxis
    print "Hubo", i, "tokens"
