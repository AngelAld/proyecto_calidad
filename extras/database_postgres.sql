CREATE TABLE IF NOT EXISTS SEMESTRE_ACADEMICO(
    id_semestre SERIAL PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    estado char(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS ROL(
    id SERIAL PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    estado CHAR(1) NOT NULL
);

INSERT INTO ROL(nombre, estado) VALUES ('Director de escuela', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Docente de Apoyo', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Estudiante', 'A');

CREATE TABLE IF NOT EXISTS USUARIO(
    id SERIAL PRIMARY KEY,
    idrol int DEFAULT NULL,
    foreign key(idrol) references rol(id),
    nombre varchar(100) DEFAULT NULL,
    usuario VARCHAR(100),
    clave text NOT NULL,
    correo varchar(100) DEFAULT NULL,
    estado CHAR(1) NOT NULL
);

INSERT INTO USUARIO(idrol, nombre, usuario, clave, correo, estado) VALUES(
    1,
    'Usuario de pruebas',
    'Admin123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'admin123@gmail.com',
    'A'
);

INSERT INTO USUARIO(idrol, nombre, usuario, clave, correo, estado) VALUES(
    2,
    'Docente de pruebas',
    'Docente123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'docente12@gmail.com',
    'A'
);



CREATE OR REPLACE FUNCTION fn_login
(p_usuario VARCHAR(20)
)
RETURNS TABLE(
	id integer, 
    idrol integer, 
    nombre VARCHAR(100), 
    usuario VARCHAR(100),
	clave text, 
    correo VARCHAR(100), 
    estado CHAR(1), 
    rol VARCHAR(50))
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	RETURN QUERY
		SELECT 
			u.*, r.nombre as rol
		FROM usuario u
			INNER JOIN rol r on r.id=u.idrol
		WHERE u.usuario=p_usuario;
END
$BODY$;

CREATE OR REPLACE FUNCTION fn_read_semestres() RETURNS TABLE (
    id_semestre INTEGER,
    nombre VARCHAR(50),
    fecha_inicio VARCHAR(10),
    fecha_fin VARCHAR(10),
    estado CHAR(1)
) AS $$ BEGIN RETURN QUERY
SELECT
    sa.id_semestre,
    sa.nombre,
    (to_char(sa.fecha_inicio, 'DD/MM/YYYY')) :: varchar AS fecha_inicio,
    (to_char(sa.fecha_fin, 'DD/MM/YYYY')) :: varchar AS fecha_fin,
    sa.estado
FROM
    SEMESTRE_ACADEMICO sa
ORDER BY
    estado,
    nombre ASC;

END;

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_create_semestre(
    p_nombre VARCHAR(50),
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_estado CHAR(1)
) RETURNS VARCHAR(255) AS $$ DECLARE semestre_existe INTEGER;

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

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_update_semestre(
    p_id_semestre INTEGER,
    p_nombre VARCHAR(50),
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_estado CHAR(1)
) RETURNS VARCHAR(255) AS $$ DECLARE semestre_existe INTEGER;

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

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_delete_semestre(p_id INTEGER) RETURNS VARCHAR(100) AS $$ DECLARE mensaje VARCHAR(100);

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

$$ LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION fn_update_estado(p_id_semestre INTEGER, p_estado CHAR(1)) RETURNS VARCHAR(255) AS $$ DECLARE error_message VARCHAR(255);

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

$$ LANGUAGE plpgsql;



------------------------------------ ##### TABLA DE INFORME INICIAL ESTUDIANTE ##### -------------------------------------
--------------------------------------------------------------------------------------------------------------------------