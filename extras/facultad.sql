CREATE OR REPLACE FUNCTION fn_listar_facultad()
  RETURNS TABLE(id_facultad integer, nombre character varying, descripcion text, estado character)
  LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN QUERY SELECT 
    f.id_facultad,
    f.nombre,
    f.descripcion,
    f.estado
  FROM FACULTAD f
  ORDER BY f.estado, f.nombre ASC;
END;
$function$;

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_consultar_facultad_ID(p_id integer)
RETURNS TABLE(id_facultad integer, nombre character varying, descripcion text, estado character)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        f.id_facultad,
        f.nombre,
        f.descripcion,
        f.estado
    FROM FACULTAD f
    WHERE f.id_facultad = p_id;
END;
$function$;

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_agregar_facultad(p_nombre character varying, p_descripcion text, p_estado character)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    facultad_existe INTEGER;
    error_message  VARCHAR(255);
    error_code     VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO facultad_existe
        FROM FACULTAD
        WHERE nombre = p_nombre;

        IF facultad_existe > 0 THEN
            RETURN 'Facultad ya existe';
        END IF;

        INSERT INTO FACULTAD (nombre, descripcion, estado)
        VALUES (p_nombre, p_descripcion, p_estado);

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

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_editar_facultad(p_id_facultad integer, p_nombre character varying, p_descripcion text, p_estado character)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  facultad_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO facultad_existe
    FROM FACULTAD
    WHERE nombre = p_nombre
      AND id_facultad != p_id_facultad;

    IF facultad_existe > 0 THEN
      RETURN 'Facultad ya existe';
    END IF;

    UPDATE FACULTAD
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        estado = p_estado
    WHERE id_facultad = p_id_facultad;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_facultad(p_id integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje VARCHAR(100);
  error_msg VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM FACULTAD
    WHERE id_facultad = p_id;

    -- Verificar si se eliminó el registro correctamente
    IF FOUND THEN
      mensaje := 'Operación realizada con éxito';
    ELSE
      RETURN 'No se pudo eliminar el registro.';
    END IF;

  EXCEPTION
    WHEN OTHERS THEN
      error_msg := CONCAT('Error: ', SQLERRM);
      RETURN '%' || error_msg;
  END;

  RETURN mensaje;
END;
$function$;

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_actualizar_estado_facultad(p_id_facultad integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE FACULTAD
        SET estado = p_estado
        WHERE id_facultad = p_id_facultad;

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
