


CREATE OR REPLACE FUNCTION fn_listar_docente_apoyo() 
RETURNS TABLE(
    id_docente_apoyo integer,
    nombre varchar(255),
    correo varchar(255),
    estado char(1),
    id_titulo integer,
    titulo_profesional varchar(255),
    id_escuela_profesional integer,
    escuela_profesional varchar(255),
    id_usuario integer
) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        da.id_docente_apoyo,
        da.nombre,
        da.correo,
        da.estado,
        da.id_titulo,
        tp.nombre AS titulo_profesional,
        da.id_escuela_profesional,
        ep.nombre AS escuela_profesional,
        da.id_usuario
    FROM 
        DOCENTE_APOYO da
        INNER JOIN TITULO_PROFESIONAL tp ON da.id_titulo = tp.id_titulo
        INNER JOIN ESCUELA_PROFESIONAL ep ON da.id_escuela_profesional = ep.id_escuela_profesional
    ORDER BY 
        da.estado, 
        da.nombre ASC;
END;
$$ LANGUAGE plpgsql;