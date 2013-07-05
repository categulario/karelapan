UPDATE usuarios_usuario SET problemas_resueltos=0, puntaje=0 WHERE true;
DELETE FROM evaluador_envio WHERE TRUE;
UPDATE evaluador_problema SET veces_resuelto=0, veces_intentado=0, mejor_tiempo=-1, mejor_puntaje=-1 WHERE TRUE;
