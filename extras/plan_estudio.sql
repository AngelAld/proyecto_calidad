CREATE OR REPLACE FUNCTION fn_listar_planEstudio()
 RETURNS TABLE(id_plan_estudio integer, nombre character varying, estado character, id_escuela_profesional integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
pe.id_plan_estudio, 
pe.nombre,
pe.estado,
pe.id_escuela_profesional
FROM PLAN_ESTUDIO pe
ORDER BY estado, nombre ASC;
END;
$function$
;


----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_consultar_plan_estudio_ID(p_id integer)
RETURNS TABLE(id_plan_estudio integer, nombre character varying, estado character, id_escuela_profesional integer)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        pe.id_plan_estudio, 
        pe.nombre,
        pe.estado,
        ld.estado,
        pe.id_escuela_profesional
    FROM PLAN_ESTUDIO pe
    WHERE pe.id_plan_estudio = p_id;
END;
$function$;



----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_agregar_plan_estudio(p_nombre character varying, p_estado character, p_id_escuela_profesional int)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    linea_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO linea_existe
        FROM PLAN_ESTUDIO
        WHERE nombre = p_nombre;

        IF linea_existe > 0 THEN
            RETURN 'Plan estudio ya existe';
        END IF;

        INSERT INTO PLAN_ESTUDIO (nombre, estado, id_escuela_profesional)
        VALUES (p_nombre, p_estado, p_id_escuela_profesional);

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


----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_editar_plan_estudio(p_id_plan_estudio integer, p_nombre character varying, p_estado character, p_id_escuela_profesional integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  plan_estudio_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO plan_estudio_existe
    FROM PLAN_ESTUDIO 
    WHERE nombre = p_nombre
      AND id_plan_estudio != p_id_plan_estudio;

    IF plan_estudio_existe > 0 THEN
      RETURN 'Plan Estudio ya existe';
    END IF;

    UPDATE PLAN_ESTUDIO
    SET nombre = p_nombre,
        estado = p_estado,
        id_plan_estudio = p_id_plan_estudio
    WHERE id_plan_estudio = p_id_plan_estudio;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;

------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_plan_estudio(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM PLAN_ESTUDIO
    WHERE id_plan_estudio = p_id;

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


------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_actualizar_estado_plan_estudio(p_id_plan_estudio integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE PLAN_ESTUDIO
        SET estado = p_estado
        WHERE id_plan_estudio = p_id_plan_estudio;

        EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
            error_code = RETURNED_SQLSTATE;

            error_message := CONCAT('Error: ', error_message);

            RETURN '%', error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$function$;



