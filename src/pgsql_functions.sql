-- Function: actualiza_puntaje_concurso(integer)

-- DROP FUNCTION actualiza_puntaje_concurso(integer);

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

-- Function: actualiza_puntaje(integer)

-- DROP FUNCTION actualiza_puntaje(integer);

CREATE OR REPLACE FUNCTION actualiza_puntaje(id_usuario integer)
  RETURNS void AS
$BODY$
    DECLARE
        problema RECORD;
        suma INTEGER;
        parcial INTEGER;
    BEGIN
        suma := 0;
        FOR problema IN SELECT DISTINCT problema_id FROM evaluador_envio WHERE usuario_id = id_usuario AND concurso_id isnull
        LOOP
            SELECT MAX(puntaje) INTO parcial FROM evaluador_envio WHERE problema_id=problema.problema_id AND usuario_id=id_usuario AND concurso_id isnull;
            suma = suma + parcial;
        END LOOP;
        UPDATE usuarios_perfil SET puntaje=suma WHERE id=(SELECT id FROM usuarios_perfil WHERE usuario_id=id_usuario);
    END;
$BODY$
    LANGUAGE plpgsql VOLATILE
    COST 100;

ALTER FUNCTION actualiza_puntaje_concurso(integer, integer)
    OWNER TO covi;

ALTER FUNCTION actualiza_puntaje(integer)
    OWNER TO covi;
