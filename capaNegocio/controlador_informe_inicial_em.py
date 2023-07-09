from capaDatos.bd import obtener_conexion
import psycopg2

def listar_informes_iniciales_empresa():
    conexion = obtener_conexion()
    informes = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas INFORME_INICIAL_ES, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT iie.id_informe_inicial_em,e.nombre,cp.razon_social,iie.estado FROM ESTUDIANTE e JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica JOIN INFORME_INICIAL_EM iie ON dp.id_detalle_practica = iie.id_detalle_practica JOIN JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato JOIN CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas"
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

def consultar_informe_iniciales_empresa(id_informe_inicial_em):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            # Obtener nombre del estudiante
            cursor.execute("""
                SELECT e.nombre
                FROM ESTUDIANTE e
                JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN INFORME_INICIAL_EM iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_em = %s
            """, (id_informe_inicial_em,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato, y cargo del jefe inmediato
            cursor.execute("""
                SELECT cp.razon_social, ji.nombre, ji.cargo
                FROM CENTRO_PRACTICAS cp
                JOIN JEFE_INMEDIATO ji ON cp.id_centro_practicas = ji.id_centro_practicas
                JOIN DETALLE_PRACTICA dp ON ji.id_jefe_inmediato = dp.id_jefe_inmediato
                JOIN INFORME_INICIAL_EM iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_em = %s
            """, (id_informe_inicial_em,))
            datos_cppp = cursor.fetchone()

            # Obtener información del detalle de práctica: fecha inicial y final
            cursor.execute("""
                SELECT dp.fecha_inicio, dp.fecha_fin
                FROM DETALLE_PRACTICA dp
                JOIN INFORME_INICIAL_EM iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_em = %s
            """, (id_informe_inicial_em,))
            datos_practica = cursor.fetchone()


            cursor.execute("SELECT * FROM informe_inicial_em WHERE id_informe_inicial_em = %s", (id_informe_inicial_em,))
            informe = cursor.fetchone()


        conexion.close()

        return estudiante, datos_cppp, datos_practica, informe

    except Exception as e:
        return f"Error al consultar informe inicial: {str(e)}"


def dar_baja_informe_inicial(p_id_informe_inicial_em, p_estado):
    try:
        conexion = obtener_conexion()

        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"

        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_actualizar_estado_informe_inicial_em(%s, %s)",
                (p_id_informe_inicial_em, new_estado),
            )

        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        return f"Error al cambiar el estado del informe: {str(e)}"


def eliminar_informe_inicial_em(id_informe_inicial_em):
    conexion = obtener_conexion()
    msg = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_eliminar_informe_inicial_em(%s)",
            (id_informe_inicial_em,),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

# def actualizar_informe_inicial_em(id_informe_inicial_em, estado, id_detalle_practica):
#     conexion = obtener_conexion()
#     msg = None
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute(
#                 " UPDATE informe_inicial_em SET compromiso = '', labores = '', firma_em = '', firma_es = '' WHERE id_informe_inicial_em = %s AND estado = %s AND id_detalle_practica = %s", 
#                 (id_informe_inicial_em, estado, id_detalle_practica),
#             )
#             msg = cursor.fetchone()
#         conexion.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         conexion.close()
#     return msg[0] if msg is not None else None


def actualizar_informe_inicial_em(firma_em, firma_es, compromiso, labores,id_informe_inicial_em):
    try:
        conexion = obtener_conexion()
        conexion.autocommit = False

        with conexion.cursor() as cursor:
            cursor.execute("UPDATE INFORME_INICIAL_EM SET firma_em = %s, firma_es = %s, compromiso = %s, labores=%s WHERE id_informe_inicial_em = %s", (id_informe_inicial_em,))

            #id_detalle_practica = cursor.fetchone()[0]

        conexion.commit()
        conexion.close()

        return "Operacion realizada con éxito"

    except Exception as e:
        conexion.rollback()
        return f"Error al cambiar el estado del informe: {str(e)}"