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

def actualizar_informe_inicial(id, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE INFORME_INICIAL_ES SET estado = %s WHERE id_informe_inicial_es = %s",
            (estado, id),
        )
        conexion.commit()
        if cursor.rowcount > 0:
            msg = ["El informe inicial se actualizó correctamente."]
        else:
            msg = ["No se encontró el informe inicial con el ID proporcionado."]
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_informe_inicial(p_id_informe_inicial_es, p_estado):
    conexion = obtener_conexion()
    msg = ""

    if p_estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"

    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_informe_inicial_es(%s, %s)", (p_id_informe_inicial_es, new_estado))
        msg = cursor.fetchone()[0]

    conexion.commit()
    conexion.close()
    return msg if msg is not None else None

def actualizar_informe_inicial_es(id_informe_inicial_es, estado, id_detalle_practica):
    conexion = obtener_conexion()
    msg = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT editar_informe_inicial_es(%s, %s, %s)",
                (id_informe_inicial_es, estado, id_detalle_practica),
            )
            msg = cursor.fetchone()
        conexion.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()
    return msg[0] if msg is not None else None

def eliminar_informe_inicial_es(id_informe_inicial_es):
    conexion = obtener_conexion()
    msg = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_eliminar_informe_inicial_es(%s)",
            (id_informe_inicial_es,),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

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

def buscar_informe_inicial_id(id):
    conexion = obtener_conexion()
    informe_inicial = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM informe_inicial WHERE id = %s",
            (id,),
        )
        informe_inicial = cursor.fetchone()
    conexion.close()
    return informe_inicial

""" def listar_centroPracticasID_informe_inicial_es():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT cp.razon_social,ji.nombre,ji.cargo FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas")
        datos_centroPracticas = cursor.fetchall()
    conexion.close()
    return datos_centroPracticas """

def calcular_puntaje_total_informe_inicial(id_estudiante):
    conexion = obtener_conexion()
    puntaje_total = 0
    datos = []
    elementos = ['firma', 'estado', 'plan de trabajo', 'otro elemento']  # Agrega aquí los elementos que deseas evaluar
    
    with conexion.cursor() as cursor:
        for elemento in elementos:
            # Obtener el conteo de informes iniciales del estudiante que contienen el elemento
            cursor.execute("SELECT COUNT(*) FROM informe_inicial_es WHERE id_estudiante = %s AND {} = 1".format(elemento), (id_estudiante,))
            conteo = cursor.fetchone()
            cantidad_informes = conteo[0]
            
            # Calcular el puntaje proporcional al número de informes que contienen el elemento
            puntaje_elemento = cantidad_informes * 5  # Cada informe con el elemento aporta 5 puntos
            puntaje_total += puntaje_elemento
            datos.append(puntaje_elemento)
    
    conexion.close()
    return puntaje_total, datos, elementos

