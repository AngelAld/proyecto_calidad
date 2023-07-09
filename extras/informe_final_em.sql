CREATE OR REPLACE FUNCTION fn_listar_informe_final_em()
RETURNS TABLE(
    id_informe_final_em integer,
    razon_social varchar(255),
    estado char(1)
)
As $$
BEGIN
    RETURN QUERY
    SELECT 
        fin_em.id_informe_final_em,
        prac.razon_social,
        fin_em.estado
    FROM
        INFORME_FINAL_EM  fin_em
        INNER JOIN DETALLE_PRACTICA detalle_prac ON detalle_prac.id_detalle_practica= fin_em.id_detalle_practica
        INNER JOIN JEFE_INMEDIATO je_in ON  je_in.id_jefe_inmediato = detalle_prac.id_jefe_inmediato
        INNER JOIN CENTRO_PRACTICAS prac ON prac.id_centro_practicas=je_in.id_centro_practicas
    ORDER BY
        fin_em.estado,
        fin_em.id_informe_final_em ASC;
END;
$$ LANGUAGE plpgsql;
------------------
CREATE OR REPLACE FUNCTION fn_buscar_nombre_informe_final_em()
RETURNS TABLE (
    razon_social varchar(255)
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        prac.razon_social
    FROM
        INFORME_FINAL_EM  fin_em
        INNER JOIN DETALLE_PRACTICA detalle_prac ON detalle_prac.id_detalle_practica= fin_em.id_detalle_practica
        INNER JOIN JEFE_INMEDIATO je_in ON  je_in.id_jefe_inmediato = detalle_prac.id_jefe_inmediato
        INNER JOIN CENTRO_PRACTICAS prac ON prac.id_centro_practicas=je_in.id_centro_practicas;
END;
$$ LANGUAGE plpgsql;
------------------error 
CREATE FUNCTION fn_agregar_informe_final_em(
    id_estudiante INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    razon_social VARCHAR(100),
    responsable_practica VARCHAR(100),
    cargo VARCHAR(50)
)RETURNS INT
BEGIN
  DECLARE informe_id INT;

  INSERT INTO InformeFinalEmpresa(id_estudiante, fecha_inicio, fecha_fin,razon_social,responsable_practica,cargo)
  VALUES (id_estudiante, fecha_inicio, fecha_fin,razon_social,responsable_practica,cargo)

  SET informe_id = LAST_INSERT_ID();
  
  RETURN informe_id;
END;
-------------------error
CREATE FUNCTION fn_actualizar_informe_final_em(
    id_estudiante INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    razon_social VARCHAR(100),
    responsable_practica VARCHAR(100),
    cargo VARCHAR(50)
)
BEGIN
  UPDATE InformeFinalEmpresa
  SET id_estudiante = id_estudiante,
      fecha_inicio = fecha_inicio,
      fecha_fin = fecha_fin,
      razon_social = razon_social,
      responsable_practica = responsable_practica,
      cargo = cargo
  WHERE informe_id = informe_id;
  
  RETURN informe_id;
END;
-------
CREATE OR REPLACE FUNCTION fn_eliminar_informe_final_em(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM INFORME_FINAL_EM
    WHERE id_informe_final_em = p_id;

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
----------
CREATE OR REPLACE FUNCTION fn_actualizar_estado_informe_final_em(p_id_informe_final_em integer, p_estado char(1))
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE INFORME_FINAL_EM
        SET estado = p_estado
        WHERE id_informe_final_em = p_id_informe_final_em;

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
------------------------
