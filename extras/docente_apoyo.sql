CREATE OR REPLACE FUNCTION fn_listar_docente_apoyo() 
RETURNS TABLE(
    id_docente_apoyo integer,
    nombre varchar(255),
    correo varchar(255),
    estado char(1),
    id_titulo integer,
    titulo_profesional varchar(255),
    id_escuela_profesional integer,
    escuela_profesional varchar(255),
    id_usuario integer
) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        da.id_docente_apoyo,
        da.nombre,
        da.correo,
        da.estado,
        da.id_titulo,
        tp.nombre AS titulo_profesional,
        da.id_escuela_profesional,
        ep.nombre AS escuela_profesional,
        da.id_usuario
    FROM 
        DOCENTE_APOYO da
        INNER JOIN TITULO_PROFESIONAL tp ON da.id_titulo = tp.id_titulo
        INNER JOIN ESCUELA_PROFESIONAL ep ON da.id_escuela_profesional = ep.id_escuela_profesional
    ORDER BY 
        da.estado, 
        da.nombre ASC;
END;
$$ LANGUAGE plpgsql;


------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_consultar_docente_apoyo_id(p_id integer)
RETURNS TABLE(
    id_docente_apoyo integer,
    nombre varchar(255),
    correo varchar(255),
    estado char(1),
    id_titulo integer,
    titulo_profesional varchar(255),
    id_escuela_profesional integer,
    escuela_profesional varchar(255),
    id_usuario integer
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        da.id_docente_apoyo,
        da.nombre,
        da.correo,
        da.estado,
        da.id_titulo,
        tp.nombre AS titulo_profesional,
        da.id_escuela_profesional,
        ep.nombre AS escuela_profesional,
        da.id_usuario
    FROM 
        DOCENTE_APOYO da
        INNER JOIN TITULO_PROFESIONAL tp ON da.id_titulo = tp.id_titulo
        INNER JOIN ESCUELA_PROFESIONAL ep ON da.id_escuela_profesional = ep.id_escuela_profesional
    WHERE 
        da.id_docente_apoyo = p_id;
END;
$function$;

------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_agregar_docente_apoyo(p_nombre character varying, p_correo character varying, p_estado character, p_id_titulo int, p_id_escuela_profesional int, p_id_usuario int)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    docente_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO docente_existe
        FROM DOCENTE_APOYO
        WHERE correo = p_correo;

        IF docente_existe > 0 THEN
            RETURN 'Docente de apoyo ya existe';
        END IF;

        INSERT INTO DOCENTE_APOYO (nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario)
        VALUES (p_nombre, p_correo, p_estado, p_id_titulo, p_id_escuela_profesional, p_id_usuario);

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

------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_editar_docente_apoyo(p_id_docente_apoyo integer, p_nombre character varying, p_correo character varying, p_estado character, p_id_titulo integer, p_id_escuela_profesional integer, p_id_usuario integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  docente_apoyo_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO docente_apoyo_existe
    FROM DOCENTE_APOYO
    WHERE nombre = p_nombre
      AND id_docente_apoyo != p_id_docente_apoyo;

    IF docente_apoyo_existe > 0 THEN
      RETURN 'Docente de apoyo ya existe';
    END IF;

    UPDATE DOCENTE_APOYO
    SET nombre = p_nombre,
        correo = p_correo,
        estado = p_estado,
        id_titulo = p_id_titulo,
        id_escuela_profesional = p_id_escuela_profesional,
        id_usuario = p_id_usuario
    WHERE id_docente_apoyo = p_id_docente_apoyo;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;


------------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_docente_apoyo(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM DOCENTE_APOYO
    WHERE id_docente_apoyo = p_id;

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


------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_actualizar_estado_docente_apoyo(p_id_docente_apoyo integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE DOCENTE_APOYO
        SET estado = p_estado
        WHERE id_docente_apoyo = p_id_docente_apoyo;

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

