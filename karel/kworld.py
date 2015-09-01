#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kworld.py
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
#
"""
Construccion de el mundo de Karel
"""
__all__ = ['contrario', 'obten_casilla_avance', 'rotado', 'kworld']

import json
from kutil import KarelException

def contrario (cardinal):
    """ Suena ridículo, pero obtiene el punto cardinal contrario al
    dado. """
    puntos = {
        'norte': 'sur',
        'sur': 'norte',
        'este': 'oeste',
        'oeste': 'este'
    }
    return puntos[cardinal]

def obten_casilla_avance (casilla, direccion):
    """ Obtiene una casilla contigua dada una casilla de inicio y
    una direccion de avance"""
    if direccion == 'norte':
        return (casilla[0]+1, casilla[1])
    elif direccion == 'sur':
        return (casilla[0]-1, casilla[1])
    elif direccion == 'este':
        return (casilla[0], casilla[1]+1)
    elif direccion == 'oeste':
        return (casilla[0], casilla[1]-1)

def rotado (cardinal):
    """ Obtiene la orientación resultado de un gira-izquierda en
    Karel """
    puntos = {
        'norte': 'oeste',
        'oeste': 'sur',
        'sur': 'este',
        'este': 'norte'
    }
    return puntos[cardinal]


class kworld(object):
    """ Representa el mundo de Karel """

    def __init__ (self, filas=100, columnas=100, karel_pos=(1,1), orientacion='norte', mochila=0, casillas=None, archivo=None, casillas_evaluacion=False):
        """ Inicializa el mundo, con Karel en la esquina 1,1 del mundo
        orientado al norte.

        El mundo es un diccionario con dos llaves:

        * karel indica mediante una tupla la fila y la columna en la que
        se encuentra el robot
        * casillas indica cómo está construido el mundo mediante un
        diccionario, que tiene por llaves las tuplas con la posicion que
        representan: (fila, columna) """
        self.mundo = {
                'karel': {
                    'posicion': karel_pos,
                    'orientacion': orientacion,
                    'mochila': mochila #Zumbadores en la mochila
                },
                'dimensiones': {
                    'filas': filas,
                    'columnas': columnas
                },
                'casillas': [casillas, dict()][casillas==None]
            }
        self.casillas_evaluacion = casillas_evaluacion #Indica cuando se trabaja con un mundo de evaluación
        if archivo is not None and isinstance(archivo, file):
            if not self.carga_archivo(archivo):
                raise KarelException("El archivo de mundo que me diste esta dañado!")

    def posicion_karel(self):
        return self.mundo['karel']['posicion']

    def establece_karel(self, posicion=(1, 1), orientacion='norte'):
        """pone a karel en algun lugar especifico"""
        self.mundo['karel']['posicion'] = posicion
        self.mundo['karel']['orientacion'] = orientacion

    def establece_mochila(self, cantidad):
        """Establece los zumbadores en la mochila de karel a cierta cantidad"""
        if cantidad == 'inf' or cantidad == '-1' or cantidad == -1:
            self.mundo['karel']['mochila'] = -1
        elif type(cantidad) == int:
            if cantidad >= 0:
                self.mundo['karel']['mochila'] = cantidad
            else:
                raise KarelException('Esta no es una cantidad apropiada de zumbadores')
        else:
            raise KarelException('Deberías consultar a un psiquiatra')

    def obten_casilla(self, coordenadas):
        """Obtiene una casilla del mundo y la devuelve así a lo sobres"""
        casilla = {
            'zumbadores': 0,
            'paredes': set()
        }
        if coordenadas[0] == 1: #Primera fila, pared izquierda
            casilla['paredes'].add('sur')
        if coordenadas[0] == 100:
            casilla['paredes'].add('norte')
        if coordenadas[1] == 1: #primera columna
            casilla['paredes'].add('oeste')
        if coordenadas[1] == 100:
            casilla['paredes'].add('este')

        if self.mundo['casillas'].has_key(coordenadas):
            casilla['zumbadores'] = self.mundo['casillas'][(coordenadas)]['zumbadores']
            casilla['paredes'] = casilla['paredes'] | self.mundo['casillas'][(coordenadas)]['paredes']

        return casilla

    def obten_mochila(self):
        """Obtiene la cantidad de zumbadores en la mochila de karel"""
        return self.mundo['karel']['mochila']

    def obten_zumbadores(self, casilla):
        """Devuelve los zumbadores para esta casilla"""
        if self.mundo['casillas'].has_key(casilla):
            return self.mundo['casillas'][casilla]['zumbadores']
        else:
            return 0

    def conmuta_pared (self, coordenadas, orientacion):
        """ Agrega una pared al mundo, si es que está permitido, el
        atributo 'coordenadas' es una tupla con la fila y columna de la
        casilla afectada, orientacion es una cadena que indica si se pone
        arriba, abajo, a la izquierda o a la derecha. """
        if 0<coordenadas[0]<self.mundo['dimensiones']['filas']+1 and 0<coordenadas[1]<self.mundo['dimensiones']['columnas']+1:
            if coordenadas[0] == 1 and orientacion == 'sur':
                return
            if coordenadas[0] == 100 and orientacion == 'norte':
                return
            if coordenadas[1] == 1 and orientacion == 'oeste':
                return
            if coordenadas[1] == 100 and orientacion == 'este':
                return
            agregar = True #Indica si agregamos o quitamos la pared
            if self.mundo['casillas'].has_key(coordenadas):
                #Puede existir una pared
                if orientacion in self.mundo['casillas'][coordenadas]['paredes']:
                    #Ya existe la pared, la quitamos
                    self.mundo['casillas'][coordenadas]['paredes'].remove(orientacion)
                    agregar = False
                else:
                    #no existe la pared, la agregamos
                    self.mundo['casillas'][coordenadas]['paredes'].add(orientacion)
            else:
                #No existe el indice, tampoco la pared, asi que se agrega
                self.mundo['casillas'].update({
                    coordenadas: {
                        'paredes': set([orientacion]),
                        'zumbadores': 0
                    }
                })
            #Debemos conmutar la pared en la casilla opuesta
            casilla_opuesta = obten_casilla_avance(coordenadas, orientacion)
            posicion_opuesta = contrario(orientacion)
            if 0<casilla_opuesta[0]<self.mundo['dimensiones']['filas']+1 and 0<casilla_opuesta[1]<self.mundo['dimensiones']['columnas']+1:
                #no es una casilla en los bordes
                if agregar:
                    #Agregamos una pared
                    if self.mundo['casillas'].has_key(casilla_opuesta):
                        #Del otro lado si existe registro
                        self.mundo['casillas'][casilla_opuesta]['paredes'].add(posicion_opuesta)
                    else:
                        #Tampoco hay registro del otro lado
                        self.mundo['casillas'].update({
                            casilla_opuesta: {
                                'paredes': set([posicion_opuesta]),
                                'zumbadores': 0
                            }
                        })
                else:
                    #quitamos una pared, asumimos que existe el registro
                    #del lado opuesto
                    self.mundo['casillas'][casilla_opuesta]['paredes'].remove(posicion_opuesta)
            #Operaciones de limpieza para ahorrar memoria
            if not (self.mundo['casillas'][coordenadas]['paredes'] or self.mundo['casillas'][coordenadas]['zumbadores']) and not self.casillas_evaluacion:
                del self.mundo['casillas'][coordenadas]
            if not (self.mundo['casillas'][casilla_opuesta]['paredes'] or self.mundo['casillas'][casilla_opuesta]['zumbadores']) and not self.casillas_evaluacion:
                del self.mundo['casillas'][casilla_opuesta]

    def pon_zumbadores (self, posicion, cantidad):
        """ Agrega zumbadores al mundo en la posicion dada """
        if cantidad == 'inf':
            cantidad = -1
        if 0<posicion[0]<self.mundo['dimensiones']['filas']+1 and 0<posicion[1]<self.mundo['dimensiones']['columnas']+1:
            if self.mundo['casillas'].has_key(posicion):
                self.mundo['casillas'][posicion]['zumbadores'] = cantidad
            else:
                self.mundo['casillas'].update({
                    posicion: {
                        'zumbadores': cantidad,
                        'paredes': set()
                    }
                })
            #Limpiamos la memoria si es necesario
            if not (self.mundo['casillas'][posicion]['paredes'] or self.mundo['casillas'][posicion]['zumbadores']) and not self.casillas_evaluacion:
                del self.mundo['casillas'][posicion]

    def avanza (self, test=False):
        """ Determina si puede karel avanzar desde la posición en la que
        se encuentra, de ser posible avanza. Si el parámetro test es
        verdadero solo ensaya. """
        #Determino primero si está en los bordes
        if self.frente_libre():
            self.mundo['karel']['posicion'] = obten_casilla_avance(self.mundo['karel']['posicion'], self.mundo['karel']['orientacion'])
            return True
        else:
            return False

    def gira_izquierda (self, test=False):
        """ Gira a Karel 90° a la izquierda, obteniendo una nueva
        orientación. Si el parámetro test es verdadero solo ensaya"""
        if not test:
            self.mundo['karel']['orientacion'] = rotado(self.mundo['karel']['orientacion'])

    def coge_zumbador (self, test=False):
        """ Determina si Karel puede coger un zumbador, si es posible lo
        toma, devuelve Falso si no lo logra. Si el parámetro test es
        verdadero solo ensaya. """
        posicion = self.mundo['karel']['posicion']
        if self.junto_a_zumbador():
            if self.mundo['casillas'][posicion]['zumbadores'] == -1:
                if not test:
                    if self.mundo['karel']['mochila'] != -1:
                        self.mundo['karel']['mochila'] += 1
            elif self.mundo['casillas'][posicion]['zumbadores']>0:
                if not test:
                    if self.mundo['karel']['mochila'] != -1:
                        self.mundo['karel']['mochila'] += 1
                    self.mundo['casillas'][posicion]['zumbadores'] -= 1
            #Limpiamos la memoria si es necesario
            if not (self.mundo['casillas'][posicion]['paredes'] or self.mundo['casillas'][posicion]['zumbadores']):
                del self.mundo['casillas'][posicion]
            return True
        else:
            return False

    def deja_zumbador (self, test=False):
        """ Determina si Karel puede dejar un zumbador en la casilla
        actual, si es posible lo deja. Si el parámetro test es verdadero
        solo ensaya  """
        posicion = self.mundo['karel']['posicion']
        if self.algun_zumbador_en_la_mochila():
            if not test:
                if self.mundo['casillas'].has_key(posicion):
                    if self.mundo['casillas'][posicion]['zumbadores'] != -1:
                        self.mundo['casillas'][posicion]['zumbadores'] += 1
                else:
                    self.mundo['casillas'].update({
                        posicion: {
                            'zumbadores': 1,
                            'paredes': set()
                        }
                    })
                if self.mundo['karel']['mochila'] != -1:
                    self.mundo['karel']['mochila'] -= 1
            return True
        else:
            return False

    def frente_libre (self):
        """ Determina si Karel tiene el frente libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        elif direccion == 'sur':
            if posicion[0] == 1:
                return False
        elif direccion == 'este':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'oeste':
            if posicion[1] == 1:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes
        else:
            if direccion in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def izquierda_libre (self):
        """ Determina si Karel tiene la izquierda libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[1] == 1:
                return False
        elif direccion == 'sur':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'este':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        elif direccion == 'oeste':
            if posicion[0] == 1:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes
        else:
            if rotado(direccion) in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def derecha_libre (self):
        """ Determina si Karel tiene la derecha libre """
        direccion = self.mundo['karel']['orientacion']
        posicion = self.mundo['karel']['posicion']
        if direccion == 'norte':
            if posicion[1] == self.mundo['dimensiones']['columnas']:
                return False
        elif direccion == 'sur':
            if posicion[1] == 1:
                return False
        elif direccion == 'este':
            if posicion[0] == 1:
                return False
        elif direccion == 'oeste':
            if posicion[0] == self.mundo['dimensiones']['filas']:
                return False
        if not self.mundo['casillas'].has_key(posicion):
            return True #No hay un registro para esta casilla, no hay paredes extra
        else:
            if rotado(rotado(rotado(direccion))) in self.mundo['casillas'][posicion]['paredes']:
                return False
            else:
                return True

    def junto_a_zumbador (self):
        """ Determina si Karel esta junto a un zumbador. """
        if self.mundo['casillas'].has_key(self.mundo['karel']['posicion']):
            if self.mundo['casillas'][self.mundo['karel']['posicion']]['zumbadores'] == -1:
                return True
            elif self.mundo['casillas'][self.mundo['karel']['posicion']]['zumbadores'] > 0:
                return True
            else:
                return False
        else:
            return False

    def orientado_al (self, direccion):
        """ Determina si karel esta orientado al norte """
        if self.mundo['karel']['orientacion'] == direccion:
            return True
        else:
            return False

    def algun_zumbador_en_la_mochila (self):
        """ Determina si karel tiene algun zumbador en la mochila """
        if self.mundo['karel']['mochila'] > 0 or self.mundo['karel']['mochila'] == -1:
            return True
        else:
            return False

    def exporta_mundo (self, nombrearchivo=False, expandir=False):
        """ Exporta las condiciones actuales del mundo usando algun
        lenguaje de marcado """
        mundo = {
            'karel': {
                'posicion': self.mundo['karel']['posicion'],
                'orientacion': self.mundo['karel']['orientacion'],
                'mochila': self.mundo['karel']['mochila']
            },
            'dimensiones': {
                'filas': self.mundo['dimensiones']['filas'],
                'columnas': self.mundo['dimensiones']['columnas']
            },
            'casillas': []
        }
        for llave, valor in self.mundo['casillas'].iteritems():
            mundo['casillas'].append({
                'fila': llave[0],
                'columna': llave[1],
                'zumbadores': valor['zumbadores'],
                'paredes': list(valor['paredes'])
            })
        if nombrearchivo:
            f = file(nombrearchivo, 'w')
            if expandir:
                f.write(json.dumps(mundo, indent=2))
            else:
                f.write(json.dumps(mundo))
            f.close()
        else:
            return mundo

    def exporta_casillas (self):
        casillas = []
        for llave, valor in self.mundo['casillas'].iteritems():
            casillas.append({
                    'fila': llave[0],
                    'columna': llave[1],
                    'zumbadores': valor['zumbadores'],
                    'paredes': list(valor['paredes'])
                })
        return casillas

    def exporta_casillas_comparacion (self):
        casillas = []
        for llave, valor in self.mundo['casillas'].iteritems():
            casillas.append({
                    'fila': llave[0],
                    'columna': llave[1],
                    'zumbadores': valor['zumbadores']
                })
        return casillas

    def carga_casillas (self, casillas):
        """ Carga las casillas de un diccionario dado. """
        self.mundo_backup_c = self.mundo
        self.mundo['casillas'] = dict()
        try:
            for casilla in casillas:
                self.mundo['casillas'].update({
                    (casilla['fila'], casilla['columna']): {
                        'zumbadores': casilla['zumbadores'],
                        'paredes': set(casilla['paredes'])
                    }
                })
        except KeyError:
            self.mundo = self.mundo_backup_c
            del(self.mundo_backup_c)
            return False
        else:
            del(self.mundo_backup_c)
            return True

    def carga_archivo (self, archivo):
        """ Carga el contenido de un archivo con la configuración del
        mundo. Archivo debe ser una instancia de 'file' o de un objeto
        con metodo 'read()'"""
        mundo = json.load(archivo)
        #Lo cargamos al interior
        self.mundo_backup = self.mundo
        try:
            self.mundo = {
                'karel': {
                    'posicion': tuple(mundo['karel']['posicion']),
                    'orientacion': mundo['karel']['orientacion'],
                    'mochila': mundo['karel']['mochila'] #Zumbadores en la mochila
                },
                'dimensiones': {
                    'filas': mundo['dimensiones']['filas'],
                    'columnas': mundo['dimensiones']['columnas']
                },
                'casillas': dict()
            }
            if not self.carga_casillas(mundo['casillas']):
                raise KarelException("Se mando un mundo deformado")
        except KeyError:
            self.mundo = self.mundo_backup
            del(self.mundo_backup)
            return False
        else:
            del(self.mundo_backup)
            return True

    def limpiar (self):
        """ Limpia el mundo y lo lleva a un estado inicial """
        self.mundo = {
            'karel': {
                'posicion': mundo['karel']['posicion'],
                'orientacion': mundo['karel']['orientacion'],
                'mochila': mundo['karel']['mochila'] #Zumbadores en la mochila
            },
            'dimensiones': {
                'filas': mundo['dimensiones']['filas'],
                'columnas': mundo['dimensiones']['columnas']
            },
            'casillas': dict()
        }

    def __str__ (self, filas=26, columnas=28):
        """Imprime bien bonito la primera porción de mundo"""
        def num_digits(a):
            if a == -1:
                return 3
            elif 0<=a <= 9:
                return 1
            elif 10<= a <= 99:
                return 2
            else:
                return 3
        def num(numero):
            if 0<=numero<=9:
                return " %d "%numero
            elif 10<=numero<=99:
                return " %d"%numero
            else:
                "%d"%numero
        columnas+=1
        karel  = {
            'norte': '^',
            'este': '>',
            'sur': 'v',
            'oeste': '<'
        }
        #s = " " + "   +"*13
        s = ""
        for i in xrange(filas, 0, -1):
            s += "\n    +"
            for j in xrange(1, columnas):
                if self.mundo['casillas'].has_key((i, j)):
                    if 'norte' in self.mundo['casillas'][(i,j)]['paredes']:
                        s += "---+"
                    else:
                        s += "   +"
                else:
                    s += "   +"
            s += "\n %s|"%num(i)
            for j in xrange(1, columnas):
                if self.mundo['karel']['posicion'] == (i, j):
                    if self.mundo['casillas'].has_key((i, j)):
                        if 'este' in self.mundo['casillas'][(i,j)]['paredes']:
                            s+= " %s |"%karel[self.mundo['karel']['orientacion']]
                        else:
                            s+= " %s  "%karel[self.mundo['karel']['orientacion']]
                    else:
                        s+= " %s  "%karel[self.mundo['karel']['orientacion']]
                elif self.mundo['casillas'].has_key((i, j)):
                    if self.mundo['casillas'][(i, j)]['zumbadores'] or (self.casillas_evaluacion):
                        digitos = num_digits(self.mundo['casillas'][(i, j)]['zumbadores'])
                        if digitos  == 1:
                            if 'este' in self.mundo['casillas'][(i,j)]['paredes']:
                                s += " %d |"%self.mundo['casillas'][(i, j)]['zumbadores']
                            else:
                                s += " %d  "%self.mundo['casillas'][(i, j)]['zumbadores']
                        elif digitos == 2:
                            if 'este' in self.mundo['casillas'][(i,j)]['paredes']:
                                s += " %d|"%self.mundo['casillas'][(i, j)]['zumbadores']
                            else:
                                s += " %d "%self.mundo['casillas'][(i, j)]['zumbadores']
                        else:
                            if 'este' in self.mundo['casillas'][(i,j)]['paredes']:
                                s += " ∞ |"
                            else:
                                s += " ∞  "
                    else:
                        if 'este' in self.mundo['casillas'][(i,j)]['paredes']:
                            s += "   |"
                        else:
                            s += "    "
                else:
                    s += "    "
        s += "\n    +" + "---+"*(columnas-1)
        s += '\n     '
        for i in xrange(1, columnas):
            if num_digits(i)==1:
                s += " %d  "%i
            else:
                s += "%d  "%i
        if self.obten_mochila() == -1:
            s += '\n mochila: infititos'
        else:
            s += '\n mochila: %d'%self.obten_mochila()
        return s


if __name__ == '__main__':
    #Pruebas
    from pprint import pprint
    casillas_prueba = {
        (1, 1) : {
            'zumbadores': -1,
            'paredes': set(['este'])
        },
        (1, 2): {
            'zumbadores': 5,
            'paredes': set(['oeste'])
        },
        (5, 5): {
            'zumbadores': -1,
            'paredes': set()
        },
        (2, 1): {
            'zumbadores': 15,
            'paredes': set()
        }
    } #Representa la estructura de un mundo consistente
    mundo = kworld()
    mundo.conmuta_pared((1, 1), 'norte')
    mundo.conmuta_pared((1, 1), 'este')
    mundo.pon_zumbadores((5, 5), -1)
    mundo.pon_zumbadores((2, 1), 15)
    mundo.pon_zumbadores((1, 1), 7)
    mundo.avanza()
    for i in xrange(3):
        mundo.gira_izquierda()
    mundo.avanza()

    print mundo
