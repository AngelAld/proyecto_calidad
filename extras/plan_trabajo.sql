
CREATE or REPLACE FUNCTION fn_listar_plan_trabajo()
RETURNS TABLE(
    id_plan_trabajo integer,
    id_informe_final_es integer,
    n_semana integer,
    fecha_inicio date,
    fecha_fin date,
    actividad varchar(255),
    num_horas integer
)
AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        pt.id_plan_trabajo,
        pt.n_semana,
        pt.fecha_inicio,
        pt.fecha_fin,
        pt.actividad,
        pt.num_horas
    FROM 
        PLAN_TRABAJO pt
        INNER JOIN INFORME_FINAL_ES ini_es ON ini_es.id_informe_inicial_es = pt.id_informe_inicial_es
    ORDER BY 
        pt.id_plan_trabajo ASC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_agregar_plan_trabajo(p_id_plan_trabajo integer, p_n_semana integer, p_fecha_inicio date, p_fecha_fin date, p_actividad varchar(255), p_num_horas integer, p_id_informe_inicial_es integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    plan_trabajo_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO plan_trabajo_existe FROM PLAN_TRABAJO where id_plan_trabajo = p_id_plan_trabajo;

        IF plan_trabajo_existe > 0 THEN
            RETURN 'Plan trabajo ya existe';
        END IF;
        INSERT INTO PLAN_TRABAJO(id_plan_trabajo, n_semana, fecha_inicio, fecha_fin, actividad, num_horas, id_informe_final_es) 
        VALUES(p_id_plan_trabajo, p_n_semana,p_fecha_inicio,p_fecha_fin,p_actividad,p_num_horas,p_id_informe_inicial_es);
    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                    error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);
            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operacion realizada con éxito';
END;
$function$;


CREATE OR REPLACE FUNCTION fn_editar_plan_trabajo(p_id_plan_trabajo integer, p_n_semana integer, p_fecha_inicio date, p_fecha_fin date, p_actividad varchar(255), p_num_horas integer, p_id_informe_inicial_es integer)
RETURNS character varying
LANGUAGE plpgsql
AS $function$
DECLARE
    plan_trabajo_existe INTEGER;
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        SELECT COUNT(*) INTO plan_trabajo_existe
        FROM PLAN_TRABAJO
        where id_plan_trabajo = p_id_plan_trabajo;

        IF plan_trabajo_existe > 0 THEN
            RETURN 'Plan trabajo ya existe';
        END IF;
        UPDATE PLAN_TRABAJO SET n_semana = p_n_semana, fecha_inicio = p_fecha_inicio, fecha_fin=p_fecha_fin, actividad=p_actividad,num_horas=p_num_horas,p_id_informe_inicial_es=p_id_informe_inicial_es
        WHERE id_plan_trabajo = p_id_plan_trabajo;
    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                    error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);
            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operacion realizada con éxito';
END;
$function$;


CREATE OR REPLACE FUNCTION fn_eliminar_plan_trabajo(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM PLAN_TRABAJO WHERE id_plan_trabajo = p_id;

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

