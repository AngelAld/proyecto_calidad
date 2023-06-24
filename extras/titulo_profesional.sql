CREATE OR REPLACE FUNCTION fn_listar_titulo_profesional()
 RETURNS TABLE(id_titulo integer, nombre character varying, descripcion character varying, estado character)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
ld.id_titulo, 
ld.nombre,
ld.descripcion,
ld.estado
FROM TITULO_PROFESIONAL ld
ORDER BY nombre ASC;
END;
$function$
;



----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_consultar_titulo_profesional_ID(p_id integer)
RETURNS TABLE(id_titulo integer, nombre character varying, descripcion character varying, estado character)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        ld.id_titulo,
        ld.nombre,
        ld.descripcion,
        ld.estado,
    FROM TITULO_PROFESIONAL ld
    WHERE ld.id_titulo = p_id;
END;
$function$;


----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_agregar_titulo_profesional(p_nombre character varying, p_descripcion character varying, p_estado character)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    titulo_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO titulo_existe
        FROM TITULO_PROFESIONAL
        WHERE nombre = p_nombre;

        IF titulo_existe > 0 THEN
            RETURN 'Titulo Profesional ya existe';
        END IF;

        INSERT INTO TITULO_PROFESIONAL (nombre, descripcion, estado)
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


----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_editar_titulo_profesional(p_id_titulo integer, p_nombre character varying, p_descripcion character varying, p_estado character)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  titulo_profesional_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO titulo_profesional_existe
    FROM TITULO_PROFESIONAL
    WHERE nombre = p_nombre
      AND id_titulo!=p_id_titulo;

    IF titulo_profesional_existe > 0 THEN
      RETURN 'Titulo Profesional ya existe';
    END IF;

    UPDATE TITULO_PROFESIONAL
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        estado = p_estado
    WHERE id_titulo = p_id_titulo;

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

CREATE OR REPLACE FUNCTION fn_eliminar_titulo_profesional(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM TITULO_PROFESIONAL
    WHERE id_titulo = p_id;

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


CREATE OR REPLACE FUNCTION fn_actualizar_estado_titulo_profesional(p_id_titulo integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE TITULO_PROFESIONAL
        SET estado = p_estado
        WHERE id_titulo = p_id_titulo;

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





