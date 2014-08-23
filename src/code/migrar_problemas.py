# -*- coding:utf-8 -*-
import _mysql
import psycopg2
from psycopg2.extras import DictCursor
from datetime import date

db=_mysql.connect("localhost","root","mai5ql","ingeniac_karel")
conn = psycopg2.connect(database="nuevocovi", user="covi", password="covipg.11")
cursor = conn.cursor(cursor_factory=DictCursor)

db.query("""SELECT * FROM problems""")
filas_problemas=db.store_result()

ids = {}

while True:
    problema = filas_problemas.fetch_row(how=1)
    if problema:
        print problema[0]['title']
        db.query("""SELECT * FROM examples WHERE problem='%s'"""%problema[0]['id'])
        filas_ejemplos=db.store_result()
        ejemplo = filas_ejemplos.fetch_row(how=1)

        cursor.execute(
            "INSERT INTO evaluador_problema (nombre, nombre_administrativo, descripcion, problema, agradecimiento, autor_id, fecha_publicacion, nivel_id, mundo, mundo_resuelto, casos_de_evaluacion, veces_resuelto, veces_intentado, mejor_tiempo, publico, futuro, logica_fuerte, limite_recursion, limite_iteracion, limite_ejecucion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                problema[0]['title'],
                problema[0]['admin_title'],
                problema[0]['description'],
                problema[0]['problem'],
                problema[0]['greeting'],
                1,
                date(int(problema[0]['date_published'][:4]), int(problema[0]['date_published'][5:7]), int(problema[0]['date_published'][8:10])),
                2,
                ejemplo[0]['world'],
                ejemplo[0]['solved_world'],
                str('pollo'),
                '0',
                '0',
                '-1',
                True,
                False,
                False,
                65000,
                65000,
                200000
            )
        )
        conn.commit()

        cursor.execute("select max(id) from evaluador_problema")
        id_problema = cursor.fetchone()[0]
        ids.update({problema[0]['id']: id_problema})
    else:
        break

db.query("""SELECT * FROM considerations""")
filas_consideraciones=db.store_result()
while True:
    consideracion = filas_consideraciones.fetch_row(how=1)
    if consideracion:
        print '\t - ', consideracion[0]['consideration']
        cursor.execute("insert into evaluador_consideracion (problema_id, texto) values (%s, %s)", (ids[consideracion[0]['problem']], consideracion[0]['consideration']))
        conn.commit()
    else:
        break
