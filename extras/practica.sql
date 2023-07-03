----------------------------------------------------------------------------CREADA---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_listar_practicas()
 RETURNS TABLE(id_practica integer,id_estudiante varchar,estado character)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
p.id_practica,
pe.nombre, 
p.estado
FROM PRACTICA p
INNER JOIN ESTUDIANTE pe ON p.id_estudiante= pe.id_estudiante 
ORDER BY pe.nombre ASC;
END;
$function$
;
----------------------------------------------------------------------CREADA----------------------------------------------
CREATE OR REPLACE FUNCTION fn_consultar_practica(p_id_practica integer)
 RETURNS TABLE(id_linea_desarrollo integer,id_estudiante integer, estado character)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
sa.id_practica,
sa.id_estudiante, 
sa.estado

FROM PRACTICA sa
WHERE sa.id_practica = p_id;
END;
$function$
;
--------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_editar_practica(
    p_id_practica INTEGER,
    p_id_estudiante INTEGER,
    p_estado CHARACTER,
    p_id_linea_desarrollo INTEGER,
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_id_semestre_academico INTEGER,
    p_horas INTEGER,
    p_id_jefe_inmediato INTEGER,
    p_informacion_adicional TEXT
)
RETURNS TEXT
LANGUAGE plpgsql
AS $function$
DECLARE
    practica_existe INTEGER;
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        SELECT COUNT(*) INTO practica_existe
        FROM practica
        WHERE id_estudiante = p_id_estudiante
          AND id_practica != p_id_practica;

        IF practica_existe > 0 THEN
            RETURN 'Ya existe una práctica asociada a ese estudiante';
        END IF;

        UPDATE practica
        SET
            id_estudiante = p_id_estudiante,
            estado = p_estado
        WHERE id_practica = p_id_practica;

        UPDATE detalle_practica
        SET
            id_linea_desarrollo = p_id_linea_desarrollo,
            fecha_inicio = p_fecha_inicio,
            fecha_fin = p_fecha_fin,
            id_semestre_academico = p_id_semestre_academico,
            horas = p_horas,
            id_jefe_inmediato = p_id_jefe_inmediato,
            informacion_adicional = p_informacion_adicional,
            estado = p_estado
        WHERE id_practica = p_id_practica;

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                       error_code = RETURNED_SQLSTATE;

            error_message := CONCAT('Error: ', error_message);
            RETURN error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$function$;

------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------CREADA------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_agregar_practica(
    p_id_estudiante VARCHAR,
    p_estado CHARACTER,
    p_id_linea_desarrollo INTEGER,
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_id_semestre_academico INTEGER,
    p_horas INTEGER,
    p_id_jefe_inmediato INTEGER,
    p_informacion_adicional TEXT
)
RETURNS TEXT
LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_practica INTEGER; -- Variable para almacenar el ID de la práctica
BEGIN
    -- Verificar si la práctica ya existe
    SELECT id_practica INTO v_id_practica
    FROM practica
    WHERE id_estudiante = p_id_estudiante;

    -- Si la práctica existe, insertar el detalle de práctica en esa práctica
    IF FOUND THEN
        INSERT INTO detalle_practica (
            id_linea_desarrollo,
            fecha_inicio,
            fecha_fin,
            id_semestre_academico,
            id_detalle_practica,
            horas,
            id_practica,
            id_jefe_inmediato,
            informacion_adicional,
            estado
        )
        VALUES (
            p_id_linea_desarrollo,
            p_fecha_inicio,
            p_fecha_fin,
            p_id_semestre_academico,
            p_horas,
            v_id_practica,
            p_id_jefe_inmediato,
            p_informacion_adicional,
            p_estado
        );
    ELSE
        -- Si la práctica no existe, crear una nueva práctica y su detalle
        BEGIN
            INSERT INTO practica (id_estudiante, estado)
            VALUES (p_id_estudiante, p_estado)
            RETURNING id_practica INTO v_id_practica;

            INSERT INTO detalle_practica (
                id_linea_desarrollo,
                fecha_inicio,
                fecha_fin,
                id_semestre_academico,
                id_detalle_practica,
                horas,
                id_practica,
                id_jefe_inmediato,
                informacion_adicional,
                estado
            )
            VALUES (
                p_id_linea_desarrollo,
                p_fecha_inicio,
                p_fecha_fin,
                p_id_semestre_academico,
                p_horas,
                v_id_practica,
                p_id_jefe_inmediato,
                p_informacion_adicional,
                p_estado
            );
        EXCEPTION
            WHEN OTHERS THEN
                -- Capturar y manejar la excepción
                RETURN 'Error al agregar la práctica y sus detalles: ' || SQLERRM;
        END;
    END IF;

    -- Si no se producen excepciones, la operación se realiza con éxito
    RETURN 'Operación realizada con éxito';
END;
$function$;



----------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_practica(p_id integer)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    mensaje VARCHAR(100);
    error_msg VARCHAR(255);
BEGIN
    BEGIN
        DELETE FROM PRACTICA
        WHERE id_practica = p_id;

        -- Verificar si se eliminó el registro correctamente
        IF FOUND THEN
            mensaje := 'Operación realizada con éxito';
        ELSE
            RETURN 'No se pudo eliminar el registro.';
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            error_msg := CONCAT('Error: ', SQLERRM);
            RETURN error_msg;  -- Devolver solo el mensaje de error
    END;

    RETURN mensaje;
END;
$function$;

----------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_actualizar_estado_practica(p_id_practica integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code INTEGER DEFAULT 99999;
BEGIN
    BEGIN
        UPDATE practica
        SET estado = p_estado
        WHERE id_practica = p_id_practica;

        EXCEPTION
            WHEN OTHERS THEN
                GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                error_code = RETURNED_SQLSTATE;

                error_message := CONCAT('Error: ', error_message);
                RETURN error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$function$;

----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_consultar_practica_por_ID(p_id_practica INTEGER)
RETURNS TABLE (
    id_detalle_practica INTEGER,
    id_practica INTEGER,
    iestudiante VARCHAR,
    estado CHARACTER,
    id_linea_desarrollo INTEGER,
    fecha_inicio DATE,
    fecha_fin DATE,
    id_centro_practicas INTEGER,
    id_semestre_academico INTEGER,
    horas INTEGER,
    id_jefe_inmediato INTEGER,
    informacion_adicional TEXT
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        dp.id_detalle_practica,
        p.id_practica,
        e.nombre,
        dp.estado,
        dp.id_linea_desarrollo,
        dp.fecha_inicio,
        dp.fecha_fin,
        cppp.id_centro_practicas,
        dp.id_semestre_academico,
        dp.horas,
        dp.id_jefe_inmediato,
        dp.informacion_adicional
    FROM
        practica p
    INNER JOIN
        detalle_practica dp ON p.id_practica = dp.id_practica 
    LEFT JOIN -- Cambio a LEFT JOIN para incluir detalles sin centro_practicas
        jefe_inmediato ji ON ji.id_jefe_inmediato = dp.id_jefe_inmediato
    LEFT JOIN -- Cambio a LEFT JOIN para incluir detalles sin centro_practicas
        centro_practicas cppp ON ji.id_centro_practicas = cppp.id_centro_practicas
    INNER JOIN -- Se une la tabla estudiante
        estudiante e ON e.id_estudiante = p.id_estudiante
    WHERE
        p.id_practica = p_id_practica;
END;
$function$;

----------------------------------------------------------
CREATE FUNCTION eliminar_detalle_practica(detalle_id INT) RETURNS BOOLEAN AS $$
DECLARE
  deleted BOOLEAN := FALSE;
BEGIN
  -- Iniciar una transacción
  BEGIN
    -- Eliminar los registros dependientes utilizando CASCADE DELETE
    DELETE FROM CONCLUSIONES WHERE id_detalle_practica = detalle_id;
    DELETE FROM ANEXOS WHERE id_detalle_practica = detalle_id;
    DELETE FROM BIBLIOGRAFIA WHERE id_detalle_practica = detalle_id;

    -- Eliminar el detalle de práctica
    DELETE FROM DETALLE_PRACTICA WHERE id_detalle_practica = detalle_id;
    
    deleted := TRUE; -- Marcar como eliminado si no se producen errores
    
    -- Confirmar la transacción si no hubo errores
    EXCEPTION WHEN others THEN
      deleted := FALSE; -- Marcar como no eliminado en caso de error
      ROLLBACK; -- Deshacer la transacción
  END;

  RETURN deleted;
END;
$$ LANGUAGE plpgsql;

