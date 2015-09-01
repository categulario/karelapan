#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  krunner.py
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
"""
Clase capaz de ejecutar archivos de Karel, tomando el resultado de un
análizis sintáctico, y un mundo.
"""

__all__ = ['merge', 'krunner']

from kworld import kworld
from kgrammar import kgrammar
from kutil import KarelException, kstack
from klexer import klexer
import sys
from collections import deque

def merge (lista_llaves, lista_valores):
    """ Combina un par de listas de la misma longitud en un
    diccionario """
    d = dict()
    l_valores = lista_valores[:]
    #Hacemos una copia de la lista, por que no queremos modificar
    #la lista original, creeme, no lo queremos...
    l_valores.reverse()
    for i in lista_llaves:
        d.update({i: l_valores.pop()})
    return d


class krunner:
    """ Ejecuta codigos compilados de Karel hasta el final o hasta
    encontrar un error relacionado con las condiciones del mundo. """
    def __init__ (self, programa_compilado, mundo=None, limite_recursion=65000, limite_iteracion=65000, limite_ejecucion=200000, debug=False):
        """ Inicializa el ejecutor dados un codigo fuente compilado y un
        mundo, tambien establece el limite para la recursion sobre una
        funcion antes de botar un error stack_overflow."""
        self.ejecutable = programa_compilado
        if mundo:
            self.mundo = mundo
        else:
            self.mundo = kworld() #En la 1,1 orientado al norte
        self.corriendo = True
        self.indice = 0 #Marcador con la posición en la cinta de ejecución
        self.ejecucion = 0 #Contador del número de instrucciones que se han ejecutado
        self.diccionario_variables = dict()

        self.sal_de_instruccion = False
        self.sal_de_bucle = False
        self.limite_recursion = limite_recursion
        self.limite_iteracion = limite_iteracion
        self.limite_ejecucion = limite_ejecucion
        self.pila = kstack() #La pila de funciones y bucles
        self.profundidad = 0
        #Las anteriores cantidades limitan que tan hondo se puede llegar
        #mediante recursion, y que tanto puede iterar un bucle, esto para
        #evitar problemas al evaluar codigos en un servidor.
        self.estado = "Ok" #El estado en que se encuentra
        self.mensaje = "" #Mensaje con que termina la ejecucion
        #Debug
        self.debug = debug

    def expresion_entera (self, valor, diccionario_variables):
        """ Obtiene el resultado de una evaluacion entera y lo devuelve
        """
        if type(valor) == dict:
            #Se trata de un sucede o un precede
            if valor.has_key('sucede'):
                return self.expresion_entera(valor['sucede'], diccionario_variables)+1
            else:
                return self.expresion_entera(valor['precede'], diccionario_variables)-1
        elif type(valor) == int:
            return valor
        else:
            #Es una variable
            return diccionario_variables[valor] #Esto debe devolver entero

    def termino_logico (self, lista_expresiones, diccionario_variables):
        """ Obtiene el resultado de la evaluacion de un termino logico 'o'
        para el punto en que se encuentre Karel al momento de la llamada,
        recibe una lista con los terminos a evaluar
        """
        for termino in lista_expresiones:
            if self.clausula_y(termino['y'], diccionario_variables):
                return True
        else:
            return False

    def clausula_y (self, lista_expresiones, diccionario_variables):
        """ Obtiene el resultado de una comparación 'y' entre terminos
        logicos """
        for termino in lista_expresiones:
            if not self.clausula_no(termino, diccionario_variables):
                return False #El resultado de una evaluacion 'y' es falso si uno de los terminos es falso
        else:
            return True

    def clausula_no (self, termino, diccionario_variables):
        """ Obtiene el resultado de una negacion 'no' o de un termino
        logico """
        if type(termino) == dict:
            #Se trata de una negacion, un 'o' o un 'si-es-cero'
            if termino.has_key('no'):
                return not self.clausula_no(termino['no'], diccionario_variables)
            elif termino.has_key('o'):
                return self.termino_logico(termino['o'], diccionario_variables)
            else:
                #Si es cero
                if self.expresion_entera(termino['si-es-cero'], diccionario_variables) == 0:
                    return True
                else:
                    return False
        else:
            #Puede ser una condicion relacionada con el mundo, o verdadero y falso
            if termino == 'verdadero':
                return True
            elif termino == 'falso':
                return False
            elif termino == 'frente-libre':
                return self.mundo.frente_libre()
            elif termino == 'frente-bloqueado':
                return not self.mundo.frente_libre()
            elif termino == 'izquierda-libre':
                return self.mundo.izquierda_libre()
            elif termino == 'izquierda-bloqueada':
                return not self.mundo.izquierda_libre()
            elif termino == 'derecha-libre':
                return self.mundo.derecha_libre()
            elif termino == 'derecha-bloqueada':
                return not self.mundo.derecha_libre()
            elif termino == 'junto-a-zumbador':
                return self.mundo.junto_a_zumbador()
            elif termino == 'no-junto-a-zumbador':
                return not self.mundo.junto_a_zumbador()
            elif termino == 'algun-zumbador-en-la-mochila':
                return self.mundo.algun_zumbador_en_la_mochila()
            elif termino == 'ningun-zumbador-en-la-mochila':
                return not self.mundo.algun_zumbador_en_la_mochila()
            else:
                #Es una preguna de orientacion
                if termino.startswith('no-'):
                    return not self.mundo.orientado_al(termino[16:]) #Que truco
                else:
                    return self.mundo.orientado_al(termino[13:]) #Oh si!

    def run (self):
        """ Ejecuta el codigo compilado de Karel en el mundo
        proporcionado, comenzando por el bloque 'main' o estructura
        principal. """
        self.step_run()
        while self.corriendo:
            self.step()

    def step_run(self):
        """Prepara las cosas para el step run"""
        self.indice = self.ejecutable['main'] #El cabezal de esta máquina de turing
        self.ejecucion = 0
        self.diccionario_variables = dict()

    def step(self):
        """Da un paso en la cinta de ejecución de Karel"""
        try:
            if self.corriendo:
                if self.ejecucion >= self.limite_ejecucion:
                    raise KarelException(u"HanoiTowerException: Tu programa nunca termina ¿Usaste 'apagate'?")
                #Hay que ejecutar la función en turno en el índice actual
                instruccion = self.ejecutable['lista'][self.indice]
                if type(instruccion) == dict:
                    #Se trata de una estructura de control o una funcion definida
                    if instruccion.has_key('si'):
                        if self.debug:
                            print 'si'
                        if self.termino_logico(instruccion['si']['argumento']['o'], self.diccionario_variables):
                            self.indice += 1 #Avanzamos a la siguiente posicion en la cinta
                        else:#nos saltamos el si, vamos a la siguiente casilla, que debe ser un sino o la siguiente instruccion
                            self.indice = instruccion['si']['fin']+1
                        self.ejecucion += 1
                    elif instruccion.has_key('sino'): #Llegamos a un sino, procedemos, no hay de otra
                        if self.debug:
                            print 'sino'
                        self.indice += 1
                        self.ejecucion += 1
                    elif instruccion.has_key('repite'):
                        if self.debug:
                            print 'repite', instruccion['repite']['argumento']
                        if not self.pila.en_tope(instruccion['repite']['id']):
                            argumento = self.expresion_entera(instruccion['repite']['argumento'], self.diccionario_variables)
                            if argumento < 0:
                                raise KarelException(u"WeirdNumberException: Estás intentando que karel repita un número negativo de veces")
                            self.pila.append({
                                'id': instruccion['repite']['id'],
                                'cuenta': 0,
                                'argumento': argumento,
                                'fin': instruccion['repite']['fin']
                            }) #Cuenta las ejecuciones para este bucle
                        if self.pila.top()['argumento']>0:
                            if self.pila.top()['cuenta'] == self.limite_iteracion:
                                raise KarelException('LoopLimitExceded: hay un bucle que se cicla')
                            self.indice += 1
                            self.pila.top()['argumento'] -= 1
                            self.pila.top()['cuenta'] += 1
                        else:#nos vamos al final y extraemos el repite de la pila
                            self.indice = instruccion['repite']['fin']+1
                            self.pila.pop()
                        self.ejecucion += 1
                    elif instruccion.has_key('mientras'):
                        if self.debug:
                            print 'mientras'
                        if not self.pila.en_tope(instruccion['mientras']['id']):
                            self.pila.append({
                                'id': instruccion['mientras']['id'],
                                'cuenta': 0,
                                'fin': instruccion['mientras']['fin']
                            }) #Cuenta las ejecuciones para este bucle
                        if self.termino_logico(instruccion['mientras']['argumento']['o'], self.diccionario_variables):#Se cumple la condición del mientras
                            if self.pila.top()['cuenta'] == self.limite_iteracion:
                                raise KarelException('LoopLimitExceded: hay un bucle que se cicla')
                            self.indice += 1
                            self.pila.top()['cuenta'] += 1
                        else:#nos vamos al final
                            self.indice = instruccion['mientras']['fin']+1
                            self.pila.pop()
                        self.ejecucion += 1
                    elif instruccion.has_key('fin'):#Algo termina aqui
                        if self.debug:
                            print 'fin', instruccion['fin']['estructura']
                        if instruccion['fin']['estructura'] in ['mientras', 'repite']:
                            self.indice = instruccion['fin']['inicio']
                        elif instruccion['fin']['estructura'] == 'si':
                            self.indice = instruccion['fin']['fin']
                        elif instruccion['fin']['estructura'] == 'sino':
                            self.indice += 1
                        else:#fin de una funcion
                            nota = self.pila.pop()#Obtenemos la nota de donde nos hemos quedado
                            self.indice = nota['posicion']+1
                            self.diccionario_variables = nota['diccionario_variables']
                            self.profundidad -= 1
                    else: #Se trata la llamada a una función
                        if self.debug:
                            print instruccion['instruccion']['nombre']
                        if self.profundidad == self.limite_recursion:
                            raise KarelException('StackOverflow: Karel ha excedido el límite de recursión')
                        #Hay que guardar la posición actual y el diccionario de variables en uso
                        self.pila.append({
                            'posicion': self.indice,
                            'diccionario_variables': self.diccionario_variables
                        })
                        self.profundidad += 1
                        # Lo que prosigue es ir a la definición de la función
                        self.indice = self.ejecutable['indice_funciones'][instruccion['instruccion']['nombre']]+1
                        # recalcular el diccionario de variables
                        valores = []
                        for i in instruccion['instruccion']['argumento']:
                            valores.append(self.expresion_entera(i, self.diccionario_variables))
                        self.diccionario_variables = merge(
                            self.ejecutable['lista'][self.indice-1][instruccion['instruccion']['nombre']]['params'],
                            valores
                        )
                        self.ejecucion += 1
                else:
                    #Es una instruccion predefinida de Karel
                    if self.debug:
                        print instruccion
                    if instruccion == 'avanza':
                        if not self.mundo.avanza():
                            raise KarelException('Karel se ha estrellado con una pared!')
                        self.indice +=1
                    elif instruccion == 'gira-izquierda':
                        self.mundo.gira_izquierda()
                        self.indice +=1
                    elif instruccion == 'coge-zumbador':
                        if not self.mundo.coge_zumbador():
                            raise KarelException('Karel quizo coger un zumbador pero no habia en su posicion')
                        self.indice +=1
                    elif instruccion == 'deja-zumbador':
                        if not self.mundo.deja_zumbador():
                            raise KarelException('Karel quizo dejar un zumbador pero su mochila estaba vacia')
                        self.indice +=1
                    elif instruccion == 'apagate':
                        self.corriendo = False #Fin de la ejecución
                        self.estado = 'OK'
                        self.mensaje = 'Ejecucion terminada'
                        return 'TERMINADO'
                    elif instruccion == 'sal-de-instruccion':
                        while self.pila.top().has_key('id'):
                            self.pila.pop() #Sacamos todos los bucles
                        nota = self.pila.pop()#Obtenemos la nota de donde nos hemos quedado
                        self.indice = nota['posicion']+1
                        self.diccionario_variables = nota['diccionario_variables']
                    elif instruccion == 'sal-de-bucle':
                        bucle = self.pila.pop()
                        self.indice = bucle['fin']+1
                    elif instruccion == 'continua-bucle':
                        bucle = self.pila.top()
                        self.indice = bucle['fin']
                    else:#FIN
                        raise KarelException(u"HanoiTowerException: Tu programa excede el límite de ejecución ¿Usaste 'apagate'?")
                    self.ejecucion += 1
            else:
                self.estado = 'OK'
                self.mensaje = 'Ejecucion terminada'
                self.corriendo = False
                return 'TERMINADO'
        except KarelException, kre:
            self.estado = 'ERROR'
            self.mensaje = kre.args[0]
            self.corriendo = False
            return 'ERROR'
        else:
            self.estado = 'OK'
            self.mensaje = 'Ejecucion terminada'
            return 'OK'

if __name__ == '__main__':
    from pprint import pprint
    from time import time
    inicio = 0
    fin = 0
    c_inicio = 0
    c_fin = 0
    if len(sys.argv) == 1:
        grammar = kgrammar(debug=False)
    else:
        fil = sys.argv[1]
        grammar = kgrammar(flujo=open(fil), archivo=fil, futuro=True)
    try:
        c_inicio = time()
        grammar.verificar_sintaxis(gen_arbol=True)
        grammar.expandir_arbol()
        c_fin = time()
    except KarelException, ke:
        print ke.args[0], "en la línea", grammar.lexer.linea, 'columna',grammar.lexer.columna
    else:
        casillas_prueba = {
            (1, 1) : {
                'zumbadores': 0,
                'paredes': set()
            }
        }
        mundo = kworld(casillas = casillas_prueba, mochila='inf')
        runner = krunner(grammar.ejecutable, mundo)

        inicio = time()
        runner.run()
        fin = time()

        pprint(runner.mundo.mundo)
        print '---'
        print runner.estado,runner.mensaje

    print "---"
    print "tiempo: ", int((c_fin-c_inicio)*1000), "milisegundos en compilar"
    print "tiempo: ", int((fin-inicio)*1000), "milisegundos en ejecutar"
    print "total:", int((c_fin-c_inicio)*1000) + int((fin-inicio)*1000), "milisegundos"

