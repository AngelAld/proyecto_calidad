CREATE OR REPLACE FUNCTION fn_listar_escuela_profesional() 
RETURNS TABLE(
    id_escuela_profesional integer,
    nombre varchar(50),
    descripcion text,
    estado char(1),
    id_facultad integer,
    nombre_facultad varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        ep.id_escuela_profesional,
        ep.nombre,
        ep.descripcion,
        ep.estado,
        ep.id_facultad,
        f.nombre AS nombre_facultad
    FROM 
        ESCUELA_PROFESIONAL ep
        INNER JOIN FACULTAD f ON ep.id_facultad = f.id_facultad
    ORDER BY 
        ep.estado, 
        ep.nombre ASC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_consultar_escuela_profesional_id(p_id integer)
RETURNS TABLE(
    id_escuela_profesional integer,
    nombre varchar(50),
    descripcion text,
    estado char(1),
    id_facultad integer,
    nombre_facultad varchar(255)
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        ep.id_escuela_profesional,
        ep.nombre,
        ep.descripcion,
        ep.estado,
        ep.id_facultad,
        f.nombre AS nombre_facultad
    FROM 
        ESCUELA_PROFESIONAL ep
        INNER JOIN FACULTAD f ON ep.id_facultad = f.id_facultad
    WHERE 
        ep.id_escuela_profesional = p_id;
END;
$function$;

CREATE OR REPLACE FUNCTION fn_agregar_escuela_profesional(p_nombre varchar(50), p_descripcion text, p_estado char(1), p_id_facultad integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    escuela_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO escuela_existe
        FROM ESCUELA_PROFESIONAL
        WHERE nombre = p_nombre;

        IF escuela_existe > 0 THEN
            RETURN 'Escuela profesional ya existe';
        END IF;

        INSERT INTO ESCUELA_PROFESIONAL (nombre, descripcion, estado, id_facultad)
        VALUES (p_nombre, p_descripcion, p_estado, p_id_facultad);

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

CREATE OR REPLACE FUNCTION fn_editar_escuela_profesional(p_id_escuela_profesional integer, p_nombre varchar(50), p_descripcion text, p_estado char(1), p_id_facultad integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
  escuela_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO escuela_existe
    FROM ESCUELA_PROFESIONAL
    WHERE nombre = p_nombre
      AND id_escuela_profesional != p_id_escuela_profesional;

    IF escuela_existe > 0 THEN
      RETURN 'Escuela profesional ya existe';
    END IF;

    UPDATE ESCUELA_PROFESIONAL
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        estado = p_estado,
        id_facultad = p_id_facultad
    WHERE id_escuela_profesional = p_id_escuela_profesional;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;

CREATE OR REPLACE FUNCTION fn_eliminar_escuela_profesional(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM ESCUELA_PROFESIONAL
    WHERE id_escuela_profesional = p_id;

    -- Verificar si se eliminó el registro correctamente
    IF FOUND THEN
      mensaje := 'Operación realizada con éxito';
    ELSE
      RETURN 'No se pudo eliminar el registro.';
    END IF;

    EXCEPTION
      WHEN OTHERS THEN
        error_msg := SQLERRM;
        mensaje := CONCAT('Error: ', error_message);
  END;

  RETURN mensaje;
END;
$function$;

