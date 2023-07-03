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
def listar_datos_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_datosEstudiante_informe_inicial_es()")
        datos_estudiante = cursor.fetchall()
    conexion.close()
    return datos_estudiante 

""" def listar_datos_estudiante(id_estudiante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * from fn_listar_datosEstudiante_informe_inicial_es()", (id_estudiante,))
        datos_estudiante = cursor.fetchall()
    conexion.close()
    return datos_estudiante """

#********************************************* Lo uso para listar los datos de centro de practicas pre profesional*
def listar_datos_centro_practica():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_datosCentroP_informe_inicial_es()")
        datos_centro_practica = cursor.fetchall()
    conexion.close()
    return datos_centro_practica

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

