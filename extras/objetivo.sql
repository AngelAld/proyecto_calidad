
CREATE or REPLACE FUNCTION fn_listar_objetivo()
RETURNS TABLE(
    id_objetivo integer,
    descripcion varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        ob.id_objetivo,
        ob.descripcion
    FROM 
        OBJETIVO ob
        INNER JOIN INFORME_INICIAL_ES ini_es ON ini_es.id_informe_inicial_es = ob.id_informe_inicial_es
    ORDER BY 
        ob.id_objetivo ASC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_agregar_objetivo(p_id_objetivo integer, p_descripcion varchar(255), p_id_informe_inicial_es integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    objetivo_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO objetivo_existe FROM OBJETIVO where id_objetivo = p_id_objetivo;

        IF objetivo_existe > 0 THEN
            RETURN 'Objetivo ya existe';
        END IF;
        INSERT INTO OBJETIVO(id_objetivo, descripcion, id_informe_inicial_es) VALUES(p_id_objetivo, p_descripcion, p_id_informe_inicial_es);
    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                    error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);
            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operacion realizada con éxito';
END;
$function$;


CREATE OR REPLACE FUNCTION fn_editar_objetivo(p_id_objetivo integer, p_descripcion varchar(255), p_id_informe_inicial_es integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    objetivo_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO objetivo_existe
        FROM OBJETIVO
        where id_objetivo = p_id_objetivo;

        IF objetivo_existe > 0 THEN
            RETURN 'Objetivo ya existe';
        END IF;
        UPDATE OBJETIVO SET descripcion = p_descripcion, id_informe_inicial_es = p_id_informe_inicial_es
        WHERE id_objetivo = p_id_objetivo;
    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                    error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);
            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operacion realizada con éxito';
END;
$function$;


CREATE OR REPLACE FUNCTION fn_eliminar_objetivo(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM OBJETIVO WHERE id_objetivo = p_id;

    -- Verificar si se eliminó el registro correctamente
    IF FOUND THEN
      mensaje := 'Operación realizada con éxito';
    ELSE
      RETURN 'No se pudo eliminar el registro.';
    END IF;

    EXCEPTION
      WHEN OTHERS THEN
        error_msg := CONCAT('Error: ', SQLERRM);
        RETURN '%', error_msg;
  END;
  RETURN mensaje;
END;
$function$;


