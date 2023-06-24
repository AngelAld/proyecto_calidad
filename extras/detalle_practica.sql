CREATE OR REPLACE FUNCTION fn_consultar_detalle_practica(p_idpractica integer)
RETURNS TABLE(
    id_detalle_practica integer,
    fecha_inicio date,
    fecha_fin date,
    informacion_adicional text,
    estado char(1),
    horas int4,
    estudiante_nombre varchar(255),
    semestre_academico_nombre varchar(255),
    CENTRO_PRACTICAS_alias varchar(255),
    JEFE_INMEDIATO_nombre varchar(255),
    LINEA_DESARROLLO_nombre varchar(255)
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT
        dp.id_detalle_practica,
        dp.fecha_inicio,
        dp.fecha_fin,
        dp.informacion_adicional,
        dp.estado,
        dp.horas,
        e.nombre AS estudiante_nombre,
        sa.nombre AS semestre_academico_nombre,
        cp.razon_social AS CENTRO_PRACTICAS_alias,
        ji.nombre AS JEFE_INMEDIATO_nombre,
        ld.nombre AS LINEA_DESARROLLO_nombre
    FROM
        DETALLE_PRACTICA dp
        INNER JOIN PRACTICA p ON dp.id_practica = p.id_practica
        INNER JOIN ESTUDIANTE e ON p.id_estudiante = e.id_estudiante
        INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato
        INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas
        INNER JOIN LINEA_DESARROLLO ld ON dp.id_linea_desarrollo = ld.id_linea_desarrollo
        INNER JOIN SEMESTRE_ACADEMICO sa ON dp.id_semestre_academico = sa.id_semestre
    WHERE
        p.id_practica = p_idpractica;
END;
$function$;