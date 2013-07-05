CREATE OR REPLACE FUNCTION actualiza_puntaje(id_usuario integer)
	RETURNS void AS
$BODY$
	DECLARE
		problema RECORD;
		suma INTEGER;
		parcial INTEGER;
	BEGIN
		suma := 0;
		FOR problema IN SELECT DISTINCT problema_id FROM evaluador_envio WHERE usuario_id = id_usuario
		LOOP
			SELECT MAX(puntaje) INTO parcial FROM evaluador_envio WHERE problema_id=problema.problema_id AND usuario_id=id_usuario;
			suma = suma + parcial;
		END LOOP;
		UPDATE usuarios_usuario SET puntaje=suma WHERE id=id_usuario;
	END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;
ALTER FUNCTION actualiza_puntaje(id_usuario integer) OWNER TO covi;