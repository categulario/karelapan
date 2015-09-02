# Karelapan

## Cómo instalar

Prerequisitos:

* python 2.7
* Virtualenv
* Postresql

Lo primero es crear un entorno virtual para karelapan, entrar en él y activarlo:

```bash
$ virtualenv karelapan_env
$ cd karelapan_env
$ source bin/activate
```

Luego clonar este repo dentro del entorno virtual

```bash
$ git clone git@bitbucket.org:developingo/karelapan.git
$ cd karelapan
```

e instalar las dependencias del proyecto

```bash
$ pip install -r requirements.txt
```

Luego hay que instalar las tablas adecuadas

```bash
$ ./manage.py syncdb --all
$ ./manage.py migrate --fake
```

Quizá en ese paso se ofrezca la posibilidad de crear un usuario, no hay que rechazarla.

En este momento sería buena idea, si es una copia de desarrollo, editar el archivo `bin/activate` dentro del entorno virtual y añadir la línea `export DJANGO_SETTINGS_MODULE="karelapan.settings_dev"` para usar el archivo de configuración alterno. Igualmente es útil añadir la línea `unset DJANGO_SETTINGS_MODULE` para desactivar esto al salir del entorno.

Para este momento deberías cargar un par de funciones que uso en postgresql para la evaluación de problemas

```bash
$ psql -d covi < src/pgsql_functions.sql
```

Y si todo sale bien, para este momento puedes arrancar el demonio evaluador de karelapan:

```bash
$ ./kareld start
```

y luego el servidor web de desarrollo:

```
$ ./manage.py runserver
```

## Producción

Aquí hay que configurar Nginx y gunicorn para comenzar a servir peticiones desde la internet, en uno de los pasos previos ya se instaló gunicorn así que lo interesante es nginx.

# KarelCore

Xalapa, Ver. 2012

## Descripción

Te gustaba tanto jugar con Karel que decidiste que lo querías en tu plataforma favorita: Linux, así que programaste como poseído en python hasta lograr que Karel corra en Linux, Windows, Mac, Solaris y cualquier otra bestia...

## Problema

Karel requiere algunas librerías privativas para correr, escribe un programa que no las requiera, y que permita ejecutar códigos de Karel en un mundo.

## Consideraciones

* Karel necesita recursión para poder resolver problemas.
* Karel se lleva muy bien con los pingüinos.
* Un autómata finito o máquina de estado finito es un modelo computacional que realiza cómputos en forma automática sobre una entrada para producir una salida.
* No importa la posición ni orientación final de Karel.

## Proyecto

Karel el robot, escrito completamente en python. Por [@Categulario](https://twitter.com/categulario)

El objetivo de este proyecto es ofrecer el lenguaje ''Karel'' orientado al aprendizaje de la programación para todas las plataformas y sin requerir librerías privativas.

Hasta el momento sólo está soportada la sintaxis 'pascal' de Karel, algunos cambios en la sintaxis pueden haber sido influenciados por la sintaxis de Python, sin embargo cualquier código en la sintaxis original de Karel será reconocido.

## Necesito ayuda!

Si conoces Karel el robot y tienes códigos escritos puedes hacer dos cosas por mi:

* Probar que los codigos sean correctamente ejecutados por el analizador sintáctico.
* Hecho lo anterior, poner un error de sintaxis en los códigos y ver si el analizador lo reconoce.
* También puedes descargar todas las fuentes y probar los componentes, ¡es divertido!

Cualquier irregularidad me avisan a a.wonderful.code@gmail.com, información sobre cómo verificar la sintaxis de los archivos está abajo.

## Comand Line Interface (CLI)

El núcleo de Karel es una utilería de consola, y la puedes utilizar muy bien como tal, el archivo más importante se llama `karel` y está en la carpeta `bin` de este repositorio, se usa como sigue:

`cd KarelCore/bin`

(Si eres un usuario avanzado te recomiendo simplemente añadir la carpeta `KarelCore/bin` a tu variable PATH)

Para correr un código basta con hacer
`$ python karel archivo.karel`
O puedes mandarle un archivo de mundo (de los nuevos, no los viejos MDO)
`$ python karel archivo.karel -m mundo.world`

Si tienes un archivo de condiciones de evaluación (.nkec) puedes usarlo como
`$ python karel test codigo.karel -m condiciones.nkec`

Es posible obtener una poca de ayuda con:

`$ python karel --help`

## TODO

Cosas importantes por hacer:

* Extender la ayuda.
* Optimizar el runner y la gramática.

Algunas buenas ideas por implementar en este proyecto:

* Poner una sección con un tutorial de Karel a modo de 'misiones'.
* Crear la sintaxis ruby de Karel.

## Notas

* Añadí (para evitar conflictos y confusiones frecuentes) soporte para 'repetir' y 'repite' como bucles, ambos con la misma funcionalidad. Cualquier comentario me avisan. (Cuando competí en la OMI no saben cuánta lata me dio esto :) )
* El operador lógico `o` de pascal tiene un amigo `u` con la misma función.
* Trato de hacer los mensajes de error lo más comprensibles posible, se aceptan comentarios.
* Ya están soportados los comentarios de la sintaxis original de Karel.
* Los procedimientos tienen soporte para varias variables, quién sabe, con suerte esto abre las puertas a mas problemas.
* Estoy usando JSON para el almacenamiento de los mundos, es la magia de los diccionarios en python.
* Se implementó la instruccion `sal-de-bucle` que rompe un ciclo, equivalente al `break` en otros lenguajes, para usarse en conjunto con las condiciones `verdadero` y `falso`.
* En `kgrammar.py` hay una directiva llamada `futuro` en el constructor, que activa las palabras `verdadero`, `falso`, `sal-de-instruccion` y `sal-de-bucle`.

Todo el desarrollo del proyecto se llevó a cabo en Debian Wheezy, Ubuntu 12.04 y OpenSUSE usando el IDE Geany (Tavira, Gromia). Otras herramientas incluyen Git como sistema de control de versiones, Git-cola como interfaz para Git, y la magia del escritorio Gnome shell!!
