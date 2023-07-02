from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    informe_inicial_es = []
    conexion.close()
    return informe_inicial_es

def listar_informe_inicial_es():
    conexion = obtener_conexion()
    informe_inicial_es = []
    with conexion.cursor() as cursor:
        cursor.execute("select ini_es.id_informe_inicial_es,es.nombre as estudiantes,ini_es.estado FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante")
        informe_inicial_es = cursor.fetchall()
    conexion.close()
    return informe_inicial_es

#********************************************* Lo uso para listar los datos de estudiante*
def obtener_nombre_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT es.id_estudiante, es.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante")
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante

def obtener_codigo_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT es.id_estudiante, es.cod_universitario FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante")
        codigo_estudiante = cursor.fetchall()
    conexion.close()
    return codigo_estudiante

def obtener_semestre_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sa.id_semestre, sa.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante INNER JOIN SEMESTRE_ACADEMICO sa ON es.id_semestre_academico_ingreso = sa.id_semestre")
        semestre_estudiante = cursor.fetchall()
    conexion.close()
    return semestre_estudiante


""" def listar_estudianteID_informe_inicial_es():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT es.nombre,es.cod_universitario,sa.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante INNER JOIN SEMESTRE_ACADEMICO sa ON es.id_semestre_academico_ingreso = sa.id_semestre")
        datos_estudiante = cursor.fetchall()
    conexion.close()
    return datos_estudiante """


#********************************************* Lo uso para listar los datos de centro de practicas pre profesional*
def obtener_razon_social_cpp():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(" SELECT cp.razon_social FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas")
        razon_social_cpp = cursor.fetchall()
    conexion.close()
    return razon_social_cpp

def obtener_nombre_responsable_practica():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ji.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas")
        nombre_responsable_practica = cursor.fetchall()
    conexion.close()
    return nombre_responsable_practica

def obtener_cargo_responsable_practica():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ji.cargo FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas")
        cargo_responsable_practica = cursor.fetchall()
    conexion.close()
    return cargo_responsable_practica


""" def listar_centroPracticasID_informe_inicial_es():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT cp.razon_social,ji.nombre,ji.cargo FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas")
        datos_centroPracticas = cursor.fetchall()
    conexion.close()
    return datos_centroPracticas """



