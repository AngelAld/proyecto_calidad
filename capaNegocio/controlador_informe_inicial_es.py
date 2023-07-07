from capaDatos.bd import obtener_conexion
import psycopg2


def listar_informes_iniciales_estudiante():
    conexion = obtener_conexion()
    informes = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas INFORME_INICIAL_ES, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT i.id_informe_inicial_es, e.cod_universitario, e.nombre, c.alias, i.estado FROM INFORME informe_inicial_es_INICIAL_ES i JOIN DETALLE_PRACTICA d ON i.id_detalle_practica = d.id_detalle_practica JOIN PRACTICA p ON d.id_practica = p.id_practica JOIN ESTUDIANTE e ON p.id_estudiante = e.id_estudiante JOIN JEFE_INMEDIATO j ON d.id_jefe_inmediato = j.id_jefe_inmediato JOIN CENTRO_PRACTICAS c ON j.id_centro_practicas = c.id_centro_practicas"
            )
            informes = cursor.fetchall()

        conexion.commit()
    except psycopg2.Error as e:
        # Captura cualquier error y devuelve un mensaje de error como string
        conexion.rollback()
        informes = f"Error al obtener informes: {e}"
    finally:
        # Cierra la conexión
        conexion.close()

    return informes


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
        cursor.execute(
            "SELECT fn_actualizar_estado_informe_inicial_es(%s, %s)",
            (p_id_informe_inicial_es, new_estado),
        )
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


# ********************************************* Lo uso para listar los datos de estudiante*
def obtener_nombre_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT es.id_estudiante, es.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante"
        )
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante


def obtener_codigo_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT es.id_estudiante, es.cod_universitario FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante"
        )
        codigo_estudiante = cursor.fetchall()
    conexion.close()
    return codigo_estudiante


def obtener_semestre_estudiante():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT sa.id_semestre, sa.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN PRACTICA pr ON pr.id_practica = dp.id_practica INNER JOIN ESTUDIANTE es ON es.id_estudiante = pr.id_estudiante INNER JOIN SEMESTRE_ACADEMICO sa ON es.id_semestre_academico_ingreso = sa.id_semestre"
        )
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


# ********************************************* Lo uso para listar los datos de centro de practicas pre profesional*
def obtener_razon_social_cpp():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            " SELECT cp.razon_social FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas"
        )
        razon_social_cpp = cursor.fetchall()
    conexion.close()
    return razon_social_cpp


def obtener_nombre_responsable_practica():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT ji.nombre FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas"
        )
        nombre_responsable_practica = cursor.fetchall()
    conexion.close()
    return nombre_responsable_practica


def obtener_cargo_responsable_practica():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT ji.cargo FROM INFORME_INICIAL_ES ini_es INNER JOIN DETALLE_PRACTICA dp ON dp.id_detalle_practica = ini_es.id_detalle_practica INNER JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas"
        )
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
    elementos = [
        "firma",
        "estado",
        "plan de trabajo",
        "otro elemento",
    ]  # Agrega aquí los elementos que deseas evaluar

    with conexion.cursor() as cursor:
        for elemento in elementos:
            # Obtener el conteo de informes iniciales del estudiante que contienen el elemento
            cursor.execute(
                "SELECT COUNT(*) FROM informe_inicial_es WHERE id_estudiante = %s AND {} = 1".format(
                    elemento
                ),
                (id_estudiante,),
            )
            conteo = cursor.fetchone()
            cantidad_informes = conteo[0]

            # Calcular el puntaje proporcional al número de informes que contienen el elemento
            puntaje_elemento = (
                cantidad_informes * 5
            )  # Cada informe con el elemento aporta 5 puntos
            puntaje_total += puntaje_elemento
            datos.append(puntaje_elemento)

    conexion.close()
    return puntaje_total, datos, elementos
