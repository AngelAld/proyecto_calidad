CREATE OR REPLACE FUNCTION fn_listar_jefe_inmediato() 
RETURNS TABLE(
    id_jefe_inmediato integer,
    nombre varchar(255),
    correo varchar(255),
    telefono varchar(12),
    cargo varchar(255),
    estado char(1),
    id_centro_practicas integer,
    razon_social varchar(255),
    alias varchar(50)
) AS $$
BEGIN 
    RETURN QUERY 
    SELECT 
        ji.id_jefe_inmediato,
        ji.nombre,
        ji.correo,
        ji.telefono,
        ji.cargo,
        ji.estado,
        ji.id_centro_practicas,
        cp.razon_social,
        cp.alias
    FROM 
        JEFE_INMEDIATO ji
        INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas
    ORDER BY 
        ji.nombre ASC;
END;
$$ LANGUAGE plpgsql;
-------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_consultar_jefe_inmediato_ID(p_id integer)
RETURNS TABLE(id_jefe_inmediato integer, nombre varchar, correo varchar, telefono varchar, cargo varchar, estado char, id_centro_practicas integer, razon_social varchar, alias varchar)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        ji.id_jefe_inmediato,
        ji.nombre,
        ji.correo,
        ji.telefono,
        ji.cargo,
        ji.estado,
        ji.id_centro_practicas,
        cp.razon_social,
        cp.alias
    FROM JEFE_INMEDIATO ji
    WHERE ji.id_jefe_inmediato = p_id;
END;
$function$;

--------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_editar_jefe_inmediato(
  p_id_jefe_inmediato integer,
  p_nombre varchar(255),
  p_correo varchar(255),
  p_telefono varchar(12),
  p_cargo varchar(255),
  p_estado char(1),
  p_id_centro_practicas integer
)
RETURNS varchar(255)
LANGUAGE plpgsql
AS $function$
DECLARE
  jefe_existe INTEGER;
  error_message VARCHAR(255);
  error_code INTEGER DEFAULT 99999;
BEGIN
  BEGIN
    SELECT COUNT(*) INTO jefe_existe
    FROM JEFE_INMEDIATO
    WHERE nombre = p_nombre
      AND id_jefe_inmediato != p_id_jefe_inmediato;

    IF jefe_existe > 0 THEN
      RETURN 'Jefe inmediato ya existe';
    END IF;

    UPDATE JEFE_INMEDIATO
    SET nombre = p_nombre,
        correo = p_correo,
        telefono = p_telefono,
        cargo = p_cargo,
        estado = p_estado,
        id_centro_practicas = p_id_centro_practicas
    WHERE id_jefe_inmediato = p_id_jefe_inmediato;

    EXCEPTION WHEN OTHERS THEN
      GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                             error_code = RETURNED_SQLSTATE;

      error_message := CONCAT('Error: ', error_message);
      RETURN '%', error_message;
  END;

  RETURN 'Operación realizada con éxito';
END;
$function$;

---------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_jefe_inmediato(p_id integer)
RETURNS text
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
  id_usu integer;
BEGIN
  BEGIN
    -- Eliminar el registro correspondiente al jefe inmediato
    SELECT id_usuario INTO id_usu FROM JEFE_INMEDIATO WHERE id_jefe_inmediato = p_id;
    DELETE FROM JEFE_INMEDIATO WHERE id_jefe_inmediato = p_id;
    DELETE FROM USUARIO WHERE id_usuario = id_usu;
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

----------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_actualizar_estado_jefe_inmediato(p_id_jefe_inmediato integer, p_estado char(1))
 RETURNS varchar(255)
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE JEFE_INMEDIATO
        SET estado = p_estado
        WHERE id_jefe_inmediato = p_id_jefe_inmediato;

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