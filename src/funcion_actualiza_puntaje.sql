CREATE OR REPLACE FUNCTION actualiza_puntaje_concurso(id_usuario integer, id_concurso integer)
  RETURNS void AS
$BODY$
	DECLARE
		problema RECORD;
		suma INTEGER;
		parcial INTEGER;
	BEGIN
		suma := 0;
		FOR problema IN SELECT DISTINCT problema_id FROM evaluador_envio WHERE usuario_id = id_usuario AND concurso_id = id_concurso
		LOOP
			SELECT MAX(puntaje) INTO parcial FROM evaluador_envio WHERE problema_id=problema.problema_id AND usuario_id=id_usuario AND concurso_id = id_concurso;
			suma = suma + parcial;
		END LOOP;
		UPDATE evaluador_participacion SET puntaje=suma WHERE usuario_id=id_usuario AND concurso_id=id_concurso;
	END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION actualiza_puntaje_concurso(integer, integer)
  OWNER TO covi;