CREATE
OR REPLACE FUNCTION fn_listar_docente_apoyo() RETURNS TABLE(
    id_docente_apoyo integer,
    nombre varchar(255),
    correo varchar(255),
    titulo varchar(255),
    escuela_profesional varchar(50),
    usuario varchar(50),
    estado char(1)
) AS $$ BEGIN RETURN QUERY
SELECT
    da.id_docente_apoyo,
    da.nombre,
    da.correo,
    ti.nombre :: varchar AS titulo,
    ep.nombre :: varchar AS escuela_profesional,
    us.usuario :: varchar AS usuario,
    da.estado
FROM
    DOCENTE_APOYO da
    INNER JOIN
        titulo ti
        ON 
            ti.id_titulo = da.id_titulo
    INNER JOIN
        escuela_profesional ep
        ON 
            ep.id_escuela_profesional = da.id_escuela_profesional
    INNER JOIN
        usuario us
        ON 
            us.id_usuario = us.id_usuario
ORDER BY
    da.estado,
    da.nombre ASC;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_agregar_docente_apoyo(
    p_nombre varchar(255),
    p_correo varchar(255),
    p_titulo varchar(255),
    p_escuela_profesional varchar(50),
    p_usuario varchar(50),
    p_estado char(1)
) 
RETURNS varchar (255) AS $$ 

DECLARE docente_existe integer;
    error_message varchar(255);
    error_code varchar(5) DEFAULT '99999';
BEGIN
SELECT
    COUNT(*) INTO docente_existe
FROM
    DOCENTE_APOYO
WHERE
    nombre = p_nombre;
IF docente_existe > 0 THEN RETURN 'Docente ya existe';
END IF;
INSERT INTO
    DOCENTE_APOYO(nombre, correo, id_titulo, id_escuela_profesional, id_usuario, estado)
VALUES
    (p_nombre, p_correo, p_titulo, p_escuela_profesional, p_usuario, p_estado);

EXCEPTION
WHEN OTHERS THEN GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
error_code = RETURNED_SQLSTATE;

error_message := CONCAT('Error: ', error_message);

RETURN '%',
error_message;

END;

RETURN 'Operación realizada con éxito';

END;

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_update_docente(
    p_id_docente_apoyo integer,
    p_nombre varchar(255),
    p_correo varchar(255),
    p_titulo varchar(255),
    p_escuela_profesional varchar(50),
    p_usuario varchar(50),
    p_estado char(1)
) RETURNS varchar (255) AS $$ DECLARE docente_existe integer;

error_message varchar(255);

error_code integer DEFAULT '99999';

BEGIN BEGIN
SELECT
    COUNT(*) INTO docente_existe
FROM
    DOCENTE_APOYO
WHERE
    nombre = p_nombre
    AND id_docente_apoyo != p_id_docente_apoyo;

IF docente_existe > 0 THEN RETURN 'Docente ya existe';

END IF;

UPDATE
    DOCENTE_APOYO
SET
    nombre = p_nombre,
    correo = p_correo,
    titulo = p_titulo,
    escuela_profesional = p_escuela_profesional,
    usuario = p_usuario,
    estado = p_estado
WHERE
    id_semestre_academico = p_id_semestre_academico;

EXCEPTION
WHEN OTHERS THEN GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
error_code = RETURNED_SQLSTATE;

error_message := CONCAT('Error: ', error_message);

RETURN '%',
error_message;

END;

RETURN 'Operación realizada con éxito';

END;

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_delete_docente(p_id integer) RETURNS varchar (100) AS $$ DECLARE mensaje varchar(100);

error_msg varchar(100);

BEGIN BEGIN
DELETE FROM
    DOCENTE_APOYO
WHERE
    id_docente_apoyo = p_id;

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

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_update_estado(
    p_id_docente_apoyo integer,
    p_estado char(1)
) RETURNS varchar (255) AS $$ DECLARE error_message varchar(255);

error_code integer DEFAULT 99999;

BEGIN BEGIN
UPDATE
    DOCENTE_APOYO
SET
    estado = p_estado
WHERE
    id_docente_apoyo = p_id_docente_apoyo;

EXCEPTION
WHEN OTHERS THEN GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
error_code = RETURNED_SQLSTATE;

error_message := CONCAT('Error: ', error_message);

RETURN '%',
error_message;

END;

RETURN 'Operación realizada con éxito';

END;

$$ LANGUAGE plpgsql;