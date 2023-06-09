
CREATE OR REPLACE FUNCTION fn_actualizar_estado_informe_inicial_em(p_id_informe_inicial_em integer, p_estado char(1))
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE INFORME_INICIAL_EM
        SET estado = p_estado
        WHERE id_informe_inicial_em = p_id_informe_inicial_em;

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


CREATE OR REPLACE FUNCTION fn_eliminar_informe_inicial_em(p_id integer)
  RETURNS character varying
  LANGUAGE plpgsql
AS $function$
DECLARE
  mensaje    VARCHAR(100);
  error_msg  VARCHAR(100);
BEGIN
  BEGIN
    DELETE FROM INFORME_INICIAL_EM
    WHERE id_informe_inicial_em = p_id;

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


CREATE OR REPLACE FUNCTION editar_informe_inicial_em(
    p_id_informe_inicial_em INT,
    p_estado CHAR(1),
    p_id_detalle_practica INT,
    p_compromiso TEXT,
    p_labores TEXT,
    p_firma_em TEXT,
    p_firma_es TEXT
)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE
    error_message VARCHAR(255);
    error_code VARCHAR(5) DEFAULT '99999';
BEGIN
    BEGIN
        UPDATE informe_inicial_em
        SET compromiso = p_compromiso,
            labores = p_labores,
            firma_em = p_firma_em,
            firma_es = p_firma_es
        WHERE id = p_id_informe_inicial_em
            AND estado = p_estado
            AND id_detalle_practica= p_id_detalle_practica;

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT,
                                   error_code = RETURNED_SQLSTATE;
            error_message := CONCAT('Error: ', error_message);

            RETURN error_code || ' - ' || error_message;
    END;

    RETURN 'Operación realizada con éxito';
END;
$$;
