----------------------------------------------------------------------------CREADA---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_listar_practicas()
 RETURNS TABLE(id_practica integer, descripcion character varying, estado character, id_estudiante integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
sa.id_practica, 
sa.descripcion,
sa.estado,
sa.id_estudiante
FROM PRACTICA sa
ORDER BY estado, nombre ASC;
END;
$function$
;
----------------------------------------------------------------------CREADA----------------------------------------------
CREATE OR REPLACE FUNCTION fn_consultar_practica(p_id integer)
 RETURNS TABLE(id_practica integer, descripcion character varying, estado character, id_estudiante integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
sa.id_practica, 
sa.descripcion,
sa.estado,
sa.id_estudiante
FROM PRACTICA sa
WHERE sa.id_practica = p_id;
END;
$function$
;
--------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_editar_practica(p_id_practica integer, p_descripcion character varying, p_estado character, p_id_estudiante integer)
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
    descripcion = p_descripcion 
    AND id_practica != p_id_practica;

IF practica_existe > 0 THEN RETURN 'practica ya existe';

END IF;

UPDATE
    PRACTICA
SET
    descripcion = p_descripcion,
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
CREATE OR REPLACE FUNCTION fn_agregar_practica(p_id_estudiante integer, p_descripcion character varying, p_estado character )
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE practica_existe INTEGER;

error_message VARCHAR(255);

error_code VARCHAR(5) DEFAULT '99999';

BEGIN BEGIN
SELECT
    COUNT(*) INTO practica_existe
FROM
    PRACTICA
WHERE
    id_estudiante = p_id_estudiante;   

IF practica_existe > 0 THEN RETURN 'Practica ya existe';

END IF;

INSERT INTO
    PRACTICA (id_estudiante, descripcion, estado)
VALUES
    (p_id_estudiante,p_descripcion,p_estado);

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