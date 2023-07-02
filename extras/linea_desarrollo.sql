CREATE OR REPLACE FUNCTION fn_listar_linea_desarrollo()
 RETURNS TABLE(id_linea_desarrollo integer, nombre character varying, descripcion character varying, estado character, id_escuela_profesional integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
ld.id_linea_desarrollo, 
ld.nombre,
ld.descripcion,
ld.estado,
ld.id_escuela_profesional
FROM LINEA_DESARROLLO ld
ORDER BY estado, nombre ASC;
END;
$function$
;


----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_consultar_linea_desarrollo_ID(p_id integer)
RETURNS TABLE(id_linea_desarrollo integer, nombre character varying, descripcion character varying, estado character, id_escuela_profesional integer)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        ld.id_linea_desarrollo,
        ld.nombre,
        ld.descripcion,
        ld.estado,
        ld.id_escuela_profesional
    FROM LINEA_DESARROLLO ld
    WHERE ld.id_linea_desarrollo = p_id;
END;
$function$;



----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_agregar_linea_desarrollo(p_nombre character varying, p_descripcion character varying, p_estado character, p_id_escuela_profesional int)
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
        FROM LINEA_DESARROLLO
        WHERE nombre = p_nombre;

        IF linea_existe > 0 THEN
            RETURN 'Línea de desarrollo ya existe';
        END IF;

        INSERT INTO LINEA_DESARROLLO (nombre, descripcion, estado, id_escuela_profesional)
        VALUES (p_nombre, p_descripcion, p_estado, p_id_escuela_profesional);

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

CREATE OR REPLACE FUNCTION fn_editar_linea_desarrollo(p_id_linea_desarrollo integer, p_nombre character varying, p_descripcion character varying, p_estado character, p_id_escuela_profesional integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  linea_desarrollo_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO linea_desarrollo_existe
    FROM LINEA_DESARROLLO
    WHERE nombre = p_nombre
      AND id_linea_desarrollo != p_id_linea_desarrollo;

    IF linea_desarrollo_existe > 0 THEN
      RETURN 'Línea de desarrollo ya existe';
    END IF;

    UPDATE LINEA_DESARROLLO
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        estado = p_estado,
        id_escuela_profesional = p_id_escuela_profesional
    WHERE id_linea_desarrollo = p_id_linea_desarrollo;

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

CREATE OR REPLACE FUNCTION fn_eliminar_linea_desarrollo(p_id integer)
  RETURNS text
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM LINEA_DESARROLLO
    WHERE id_linea_desarrollo = p_id;

    -- Verificar si se eliminó el registro correctamente
    IF FOUND THEN
      mensaje := 'Operación realizada con éxito';
    ELSE
      RETURN 'No se pudo eliminar el registro.';
    END IF;

    EXCEPTION
    WHEN OTHERS THEN
      RETURN  error_msg;     
  END;
  RETURN mensaje;
END;
$function$;

------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_actualizar_estado_linea_desarrollo(p_id_linea_desarrollo integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE LINEA_DESARROLLO
        SET estado = p_estado
        WHERE id_linea_desarrollo = p_id_linea_desarrollo;

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



