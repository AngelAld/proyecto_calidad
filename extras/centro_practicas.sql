CREATE OR REPLACE FUNCTION fn_listar_centro_practica()
RETURNS TABLE (
    id_centro_practicas integer,
    ruc varchar(255),
    razon_social varchar(255),
    alias varchar(50),
    rubro varchar(255),
    telefono varchar(12),
    correo varchar(255),
    id_ubicacion integer
)
AS $$
BEGIN
    RETURN QUERY SELECT cp.id_centro_practicas, cp.ruc, cp.razon_social, cp.alias, cp.rubro, cp.telefono, cp.correo, cp.id_ubicacion
    FROM CENTRO_PRACTICAS cp;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_consultar_centroPPP_ID(p_id integer)
RETURNS TABLE(id_centro_practicas integer,
    ruc varchar(255),
    razon_social varchar(255),
    alias varchar(50),
    rubro varchar(255),
    telefono varchar(12),
    correo varchar(255),
    id_ubicacion integer)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT 
        cp.id_centro_practicas, cp.ruc, cp.razon_social, cp.alias, cp.rubro, cp.telefono, cp.correo, cp.id_ubicacion
    FROM CENTRO_PRACTICAS cp
    WHERE cp.id_centro_practicas = p_id;
END;
$function$;

CREATE OR REPLACE FUNCTION fn_agregar_centro_practicas(
    p_ruc varchar(255),
    p_razon_social varchar(255),
    p_alias varchar(50),
    p_rubro varchar(255),
    p_telefono varchar(12),
    p_correo varchar(255)
)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    centro_practicas_existe integer;
    error_message varchar(255);
    error_code varchar(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO centro_practicas_existe
        FROM CENTRO_PRACTICAS
        WHERE ruc = p_ruc;

        IF centro_practicas_existe > 0 THEN
            RETURN 'Centro de prácticas ya existe';
        END IF;

        INSERT INTO CENTRO_PRACTICAS (ruc, razon_social, alias, rubro, telefono, correo)
        VALUES (p_ruc, p_razon_social, p_alias, p_rubro, p_telefono, p_correo);

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


CREATE OR REPLACE FUNCTION fn_editar_centro_practicas(
    p_id_centro_practicas integer,
    p_ruc varchar(255),
    p_razon_social varchar(255),
    p_alias varchar(50),
    p_rubro varchar(255),
    p_telefono varchar(12),
    p_correo varchar(255)
)
RETURNS varchar(255)
AS $$
DECLARE
    centro_practicas_existe integer;
    error_message varchar(255);
    error_code varchar(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO centro_practicas_existe
        FROM CENTRO_PRACTICAS
        WHERE ruc = p_ruc
            AND id_centro_practicas != p_id_centro_practicas;

        IF centro_practicas_existe > 0 THEN
            RETURN 'Centro de prácticas ya existe';
        END IF;

        UPDATE CENTRO_PRACTICAS
        SET ruc = p_ruc,
            razon_social = p_razon_social,
            alias = p_alias,
            rubro = p_rubro,
            telefono = p_telefono,
            correo = p_correo
        WHERE id_centro_practicas = p_id_centro_practicas;

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                   error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);

            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_eliminar_centro_practicas(p_id integer)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    mensaje varchar(100);
    error_message varchar(255);
BEGIN
    BEGIN
        DELETE FROM CENTRO_PRACTICAS
        WHERE id_centro_practicas = p_id;

        -- Verificar si se eliminó el registro correctamente
        IF FOUND THEN
            mensaje := 'Operación realizada con éxito';
        ELSE
            RETURN 'No se pudo eliminar el registro.';
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RETURN SQLERRM;
    END;

    RETURN mensaje;
END;
$function$;


CREATE OR REPLACE FUNCTION fn_actualizar_estado_centro_practicas(
    p_id_centro_practicas integer,
    p_estado varchar
)
RETURNS varchar(255)
AS $$
DECLARE
    error_message varchar(255);
    error_code varchar(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE CENTRO_PRACTICAS
        SET estado = p_estado
        WHERE id_centro_practicas = p_id_centro_practicas;

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                   error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);

            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$$ LANGUAGE plpgsql;
