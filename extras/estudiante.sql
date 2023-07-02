
CREATE OR REPLACE FUNCTION fn_listar_estudiante() 
RETURNS TABLE(
    id_estudiante integer,
    cod_universitario char(10),
    dni char(8),
    nombre varchar(255),
    correo_usat varchar(255),
    correo_personal varchar(255),
    telefono varchar(15),
    telefono2 varchar(15),
    estado char(1),
    id_usuario int4,
    id_semestre_academico_ingreso int4,
    id_plan_estudio int4,
    escuela_profesional varchar(50),
    plan_estudio varchar(50),
    facultad varchar(50)
) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        e.id_estudiante,
        e.cod_universitario,
        e.dni,
        e.nombre,
        e.correo_usat,
        e.correo_personal,
        e.telefono,
        e.telefono2,
        e.estado,
        e.id_usuario,
        e.id_semestre_academico_ingreso,
        e.id_plan_estudio,
        ep.nombre AS escuela_profesional,
        pe.nombre AS plan_estudio,
        f.nombre AS facultad
    FROM 
        ESTUDIANTE e
        INNER JOIN PLAN_ESTUDIO pe ON e.id_plan_estudio = pe.id_plan_estudio 
        INNER JOIN ESCUELA_PROFESIONAL ep ON pe.id_escuela_profesional = ep.id_escuela_profesional
        INNER JOIN FACULTAD f ON ep.id_facultad = f.id_facultad
    ORDER BY 
        e.estado, 
        e.nombre ASC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_consultar_estudiante_id(p_id integer)
RETURNS TABLE(
    id_estudiante integer,
    cod_universitario char(10),
    dni char(8),
    nombre varchar(255),
    correo_usat varchar(255),
    correo_personal varchar(255),
    telefono varchar(15),
    telefono2 varchar(15),
    estado char(1),
    id_usuario int4,
    id_semestre_academico_ingreso int4,
    id_plan_estudio int4,
    escuela_profesional varchar(50),
    plan_estudio varchar(50),
    facultad varchar(50)
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        e.id_estudiante,
        e.cod_universitario,
        e.dni,
        e.nombre,
        e.correo_usat,
        e.correo_personal,
        e.telefono,
        e.telefono2,
        e.estado,
        e.id_usuario,
        e.id_semestre_academico_ingreso,
        e.id_plan_estudio,
        ep.nombre AS escuela_profesional,
        pe.nombre AS plan_estudio,
        f.nombre AS facultad
    FROM 
        ESTUDIANTE e
        INNER JOIN PLAN_ESTUDIO pe ON e.id_plan_estudio = pe.id_plan_estudio 
        INNER JOIN ESCUELA_PROFESIONAL ep ON pe.id_escuela_profesional = ep.id_escuela_profesional
        INNER JOIN FACULTAD f ON ep.id_facultad = f.id_facultad
    WHERE 
        e.id_estudiante = p_id;
END;
$function$;

CREATE OR REPLACE FUNCTION fn_agregar_estudiante(p_cod_universitario char(10), p_dni char(8), p_nombre varchar(255), p_correo_usat varchar(255), p_correo_personal varchar(255), p_telefono varchar(15), p_telefono2 varchar(15), p_estado char(1), p_id_usuario int4, p_id_semestre_academico_ingreso int4, p_id_plan_estudio int4)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    estudiante_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO estudiante_existe
        FROM ESTUDIANTE
        WHERE dni = p_dni
        OR cod_universitarious = p_cod_universitario
        OR nombre = p_nombre;

        IF estudiante_existe > 0 THEN
            RETURN 'Estudiante ya existe';
        END IF;

        INSERT INTO ESTUDIANTE (cod_universitario, dni, nombre, correo_usat, correo_personal, telefono, telefono2, estado, id_usuario, id_semestre_academico_ingreso, id_plan_estudio)
        VALUES (p_cod_universitario, p_dni, p_nombre, p_correo_usat, p_correo_personal, p_telefono, p_telefono2, p_estado, p_id_usuario, p_id_semestre_academico_ingreso, p_id_plan_estudio);

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

CREATE OR REPLACE FUNCTION fn_editar_estudiante(p_id_estudiante integer, p_cod_universitario char(10), p_dni char(8), p_nombre varchar(255), p_correo_usat varchar(255), p_correo_personal varchar(255), p_telefono varchar(15), p_telefono2 varchar(15), p_estado char(1), p_id_usuario int4, p_id_semestre_academico_ingreso int4, p_id_plan_estudio int4)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  estudiante_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO estudiante_existe
    FROM ESTUDIANTE
    WHERE dni = p_dni
      AND id_estudiante != p_id_estudiante;

    IF estudiante_existe > 0 THEN
      RETURN 'Estudiante ya existe';
    END IF;

    UPDATE ESTUDIANTE
    SET cod_universitario = p_cod_universitario,
        dni = p_dni,
        nombre = p_nombre,
        correo_usat = p_correo_usat,
        correo_personal = p_correo_personal,
        telefono = p_telefono,
        telefono2 = p_telefono2,
        estado = p_estado,
        id_usuario = p_id_usuario,
        id_semestre_academico_ingreso = p_id_semestre_academico_ingreso,
        id_plan_estudio = p_id_plan_estudio
    WHERE id_estudiante = p_id_estudiante;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;


CREATE OR REPLACE FUNCTION fn_eliminar_estudiante(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
  id_usu integer;
BEGIN
  BEGIN

    SELECT id_usuario INTO id_usu FROM ESTUDIANTE WHERE id_estudiante = p_id;
    DELETE FROM ESTUDIANTE
    WHERE id_estudiante = p_id;
    DELETE FROM USUARIO WHERE id_usuario = id_usu;

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


CREATE OR REPLACE FUNCTION fn_actualizar_estado_estudiante(p_id_estudiante integer, p_estado char(1))
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE ESTUDIANTE
        SET estado = p_estado
        WHERE id_estudiante = p_id_estudiante;

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