
CREATE or REPLACE FUNCTION fn_listar_informe_inicial_es()
RETURNS TABLE(
    id_informe_inicial_es integer,
    estado char(1),
    nombre_estudiante varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        ini_es.id_informe_inicial_es,
        es.nombre as estudiantes,
        ini_es.estado
    FROM 
        INFORME_INICIAL_ES ini_es
        INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica
        INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica
        INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante
    ORDER BY 
        ini_es.estado, 
        es.nombre ASC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_agregar_informe_inicial_es(p_id_informe_inicial_es integer, p_estado char(1), p_id_detalle_practica integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    informe_inicial_es_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO informe_inicial_es_existe
        FROM INFORME_INICIAL_ES
        where id_informe_inicial_es = p_id_informe_inicial_es;

        IF informe_inicial_es_existe > 0 THEN
            RETURN 'Informe inicial estudiante ya existe';
        END IF;
        INSERT INTO INFORME_INICIAL_ES(id_informe_inicial_es, estado, id_detalle_practica) VALUES(p_id_informe_inicial_es, p_estado, p_id_detalle_practica);
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


CREATE OR REPLACE FUNCTION fn_editar_informe_inicial_es(p_id_informe_inicial_es integer, p_estado char(1), p_id_detalle_practica integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    informe_inicial_es_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO informe_inicial_es_existe
        FROM INFORME_INICIAL_ES
        where id_informe_inicial_es = p_id_informe_inicial_es;

        IF informe_inicial_es_existe > 0 THEN
            RETURN 'Informe inicial estudiante ya existe';
        END IF;
        UPDATE INFORME_INICIAL_ES
        SET estado = p_estado,
            id_detalle_practica = p_id_detalle_practica
        WHERE id_informe_inicial_es = p_id_informe_inicial_es;
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


CREATE OR REPLACE FUNCTION fn_eliminar_informe_inicial_es(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM INFORME_INICIAL_ES
    WHERE id_informe_inicial_es = p_id;

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


CREATE OR REPLACE FUNCTION fn_actualizar_estado_informe_inicial_es(p_id_informe_inicial_es integer, p_estado char(1))
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE INFORME_INICIAL_ES
        SET estado = p_estado
        WHERE id_informe_inicial_es = p_id_informe_inicial_es;

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                   error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);

            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$function$;