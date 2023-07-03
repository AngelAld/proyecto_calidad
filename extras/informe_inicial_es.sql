
CREATE or REPLACE FUNCTION fn_listar_informe_inicial_es()
RETURNS TABLE(
    id_informe_inicial_es integer,
    estado char(1),
    nombre_estudiante varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        ini_es.id_informe_inicial_es,
        es.nombre as estudiantes,
        ini_es.estado
    FROM 
        INFORME_INICIAL_ES ini_es
        INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica
        INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica
        INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante
    ORDER BY 
        ini_es.estado, 
        es.nombre ASC;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------------------------------------------------------------------
CREATE or REPLACE FUNCTION fn_buscar_estudianteID_informe_inicial_es()
RETURNS TABLE(
	nombres varchar(255),
	codigo char(10),
    semestre varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        es.nombre,
		es.cod_universitario,
        sa.nombre
    FROM 
        INFORME_INICIAL_ES ini_es
        INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica
        INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica
        INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante
		INNER JOIN SEMESTRE_ACADEMICO sa ON es.id_semestre_academico_ingreso = sa.id_semestre;
END;
$$ LANGUAGE plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--select * from fn_buscar_estudianteID_informe_inicial_es()

CREATE or REPLACE FUNCTION fn_buscar_centroPracticaID_informe_inicial_es()
RETURNS TABLE(
	razon_social varchar(255),
	responsable varchar(355),
    cargo varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        cp.razon_social,
		ji.nombre,
        ji.cargo
    FROM 
        INFORME_INICIAL_ES ini_es
        INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica
        INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato
		INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas;
END;
$$ LANGUAGE plpgsql;
-- select * from fn_buscar_centroPracticaID_informe_inicial_es()


CREATE FUNCTION fn_agregar_informe_inicial_es(
  estudiante_id INT,
  codigo VARCHAR(50),
  semestre VARCHAR(50),
  razon_social VARCHAR(100),
  responsable_practica VARCHAR(100),
  cargo VARCHAR(50),
  fecha_inicio DATE,
  fecha_fin DATE
) RETURNS INT
BEGIN
  DECLARE informe_id INT;
  
  INSERT INTO InformeInicialEstudiante (estudiante_id, codigo, semestre, razon_social, responsable_practica, cargo, fecha_inicio, fecha_fin)
  VALUES (estudiante_id, codigo, semestre, razon_social, responsable_practica, cargo, fecha_inicio, fecha_fin);
  
  SET informe_id = LAST_INSERT_ID();
  
  RETURN informe_id;
END;

-- Función para actualizar un registro de informe inicial de estudiante
CREATE FUNCTION fn_actualizar_informe_inicial_es(
  informe_id INT,
  estudiante_id INT,
  codigo VARCHAR(50),
  semestre VARCHAR(50),
  razon_social VARCHAR(100),
  responsable_practica VARCHAR(100),
  cargo VARCHAR(50),
  fecha_inicio DATE,
  fecha_fin DATE
)
BEGIN
  UPDATE InformeInicialEstudiante
  SET estudiante_id = estudiante_id,
      codigo = codigo,
      semestre = semestre,
      razon_social = razon_social,
      responsable_practica = responsable_practica,
      cargo = cargo,
      fecha_inicio = fecha_inicio,
      fecha_fin = fecha_fin
  WHERE informe_id = informe_id;
  
  RETURN informe_id;
END;


CREATE OR REPLACE FUNCTION fn_eliminar_informe_inicial_es(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM INFORME_INICIAL_ES
    WHERE id_informe_inicial_es = p_id;

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


CREATE OR REPLACE FUNCTION fn_actualizar_estado_informe_inicial_es(p_id_informe_inicial_es integer, p_estado char(1))
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE INFORME_INICIAL_ES
        SET estado = p_estado
        WHERE id_informe_inicial_es = p_id_informe_inicial_es;

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













--------------------------------------------------------------------------
CREATE or REPLACE FUNCTION fn_listar_datosEstudiante_informe_inicial_es()
RETURNS TABLE(
	nombre varchar(255),
	codigo  char(10),
  semestre varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        es.nombre,es.cod_universitario,sa.nombre as semestre
    FROM PRACTICA p 
		INNER JOIN ESTUDIANTE es ON es.id_estudiante = p.id_estudiante
		INNER JOIN SEMESTRE_ACADEMICO SA ON sa.id_semestre = es.id_semestre_academico_ingreso
		INNER JOIN DETALLE_PRACTICA dp ON dp.id_practica = p.id_practica;
END;
$$ LANGUAGE plpgsql;

CREATE or REPLACE FUNCTION fn_listar_datosCentroP_informe_inicial_es()
RETURNS TABLE(
	nombres varchar(255),
	nombre  varchar(255),
  cargo varchar(255),
	fecha_inicio date,
	fecha_fin date
)
AS $$ 
BEGIN 
    RETURN QUERY 
 SELECT 
        cp.razon_social,ji.nombre,ji.cargo,dp.fecha_inicio,dp.fecha_fin
    FROM PRACTICA p 
		INNER JOIN ESTUDIANTE es ON es.id_estudiante = p.id_estudiante
		INNER JOIN DETALLE_PRACTICA dp ON dp.id_practica = p.id_practica
		INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato 
		INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas;
END;
$$ LANGUAGE plpgsql;