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
CREATE OR REPLACE FUNCTION fn_editar_practica(p_id_practica integer,p_id_estudiante integer,p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE practica_existe INTEGER;

error_message VARCHAR(255);

error_code INTEGER DEFAULT 99999;

BEGIN BEGIN
SELECT
    COUNT(*) INTO practica_existe
FROM
    PRACTICA
WHERE
id_practica != p_id_practica;

IF practica_existe > 0 THEN RETURN 'practica ya existe';

END IF;

UPDATE
    PRACTICA
SET
    estado = p_estado
    
WHERE
    id_practica = p_id_practica;
    id_estudiante = p_id_estudiante;

EXCEPTION
WHEN OTHERS THEN GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
error_code = RETURNED_SQLSTATE;

error_message := CONCAT('Error: ', error_message);

RETURN '%',
error_message;

END;

RETURN 'Operación realizada con éxito';

END;

$function$
;

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
RETURNS VOID
LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_practica INTEGER; -- Variable para almacenar el ID de la práctica
BEGIN
    -- Agregar la práctica
    INSERT INTO practica (id_estudiante, estado)
    VALUES (p_id_estudiante, p_estado)
    RETURNING id_practica INTO v_id_practica;

    -- Agregar los detalles de la práctica
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
        v_id_practica, -- Utilizamos la variable v_id_practica en lugar del parámetro p_id_practica
        p_id_jefe_inmediato,
        p_informacion_adicional,
        p_estado
    );
END;
$function$;



----------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION fn_eliminar_practica(p_id integer)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE mensaje VARCHAR(100);

error_msg VARCHAR(100);

BEGIN BEGIN
DELETE FROM
    PRACTICA
WHERE
    id_practica = p_id;

-- Verificar si se eliminó el registro correctamente
IF FOUND THEN mensaje := 'Operación realizada con éxito';

ELSE RETURN 'No se pudo eliminar el registro.';

END IF;

EXCEPTION
WHEN OTHERS THEN error_msg := CONCAT('Error: ', SQLERRM);

RETURN '%',
error_msg;

END;

RETURN mensaje;

END;

$function$
;
----------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_actualizar_estado_practica(p_id_practica integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE error_message VARCHAR(255);

error_code INTEGER DEFAULT 99999;

BEGIN BEGIN
UPDATE
    PRACTICA
SET
    estado = p_estado
WHERE
    id_practica = p_id_practical;

EXCEPTION
WHEN OTHERS THEN GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
error_code = RETURNED_SQLSTATE;

error_message := CONCAT('Error: ', error_message);

RETURN '%',
error_message;

END;

RETURN 'Operación realizada con éxito';

END;

$function$
;