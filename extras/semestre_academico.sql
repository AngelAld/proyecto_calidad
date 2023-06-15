CREATE OR REPLACE FUNCTION fn_listar_semestre_academico()
 RETURNS TABLE(id_semestre integer, nombre character varying, fecha_inicio character varying, fecha_fin character varying, estado character)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
sa.id_semestre, 
sa.nombre,
to_char(sa.fecha_inicio, 'DD/MM/YYYY') :: varchar AS fecha_inicio,
to_char(sa.fecha_fin, 'DD/MM/YYYY') :: varchar AS  fecha_fin,
sa.estado
FROM SEMESTRE_ACADEMICO sa
ORDER BY estado, nombre ASC;
END;
$function$
;

------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_consultar_semestre_academico_ID(p_id integer)
 RETURNS TABLE(id_semestre integer, nombre character varying, fecha_inicio date, fecha_fin date, estado character)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY SELECT 
sa.id_semestre, 
sa.nombre,
sa.fecha_inicio,
sa.fecha_fin,
sa.estado
FROM SEMESTRE_ACADEMICO sa
WHERE sa.id_semestre = p_id;
END;
$function$
;

------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_editar_semestre(p_id_semestre integer, p_nombre character varying, p_fecha_inicio date, p_fecha_fin date, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE semestre_existe INTEGER;

error_message VARCHAR(255);

error_code INTEGER DEFAULT 99999;

BEGIN BEGIN
SELECT
    COUNT(*) INTO semestre_existe
FROM
    SEMESTRE_ACADEMICO
WHERE
    nombre = p_nombre
    AND id_semestre != p_id_semestre;

IF semestre_existe > 0 THEN RETURN 'Semestre ya existe';

END IF;

IF p_fecha_fin <= p_fecha_inicio THEN RETURN 'La fecha de fin debe ser posterior a la fecha de inicio';

END IF;

UPDATE
    SEMESTRE_ACADEMICO
SET
    nombre = p_nombre,
    fecha_inicio = p_fecha_inicio,
    fecha_fin = p_fecha_fin,
    estado = p_estado
WHERE
    id_semestre = p_id_semestre;

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


------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_agregar_semestre(p_nombre character varying, p_fecha_inicio date, p_fecha_fin date, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE semestre_existe INTEGER;

fecha_actual DATE;

error_message VARCHAR(255);

error_code VARCHAR(5) DEFAULT '99999';

BEGIN BEGIN
SELECT
    COUNT(*) INTO semestre_existe
FROM
    SEMESTRE_ACADEMICO
WHERE
    nombre = p_nombre;

IF semestre_existe > 0 THEN RETURN 'Semestre ya existe';

END IF;

IF p_fecha_fin <= p_fecha_inicio THEN RETURN 'La fecha de fin debe ser posterior a la fecha de inicio';

END IF;

fecha_actual := CURRENT_DATE;

IF fecha_actual BETWEEN p_fecha_inicio
AND p_fecha_fin THEN p_estado := 'A';

END IF;

INSERT INTO
    SEMESTRE_ACADEMICO (nombre, fecha_inicio, fecha_fin, estado)
VALUES
    (p_nombre, p_fecha_inicio, p_fecha_fin, p_estado);

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

------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_eliminar_semestre(p_id integer)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE mensaje VARCHAR(100);

error_msg VARCHAR(100);

BEGIN BEGIN
DELETE FROM
    SEMESTRE_ACADEMICO
WHERE
    id_semestre = p_id;

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


------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION fn_actualizar_estado_semestre(p_id_semestre integer, p_estado character)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$ DECLARE error_message VARCHAR(255);

error_code INTEGER DEFAULT 99999;

BEGIN BEGIN
UPDATE
    SEMESTRE_ACADEMICO
SET
    estado = p_estado
WHERE
    id_semestre = p_id_semestre;

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