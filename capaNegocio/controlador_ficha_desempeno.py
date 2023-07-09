from capaDatos.bd import obtener_conexion
import psycopg2

def listar_fichas_desempeno():
    conexion = obtener_conexion()
    fichas = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas FICHA_DESEMPENO, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT f.id_ficha_desempeno, e.cod_universitario, e.nombre, c.alias, f.estado FROM ficha_desempeno f JOIN DETALLE_PRACTICA d ON f.id_detalle_practica = d.id_detalle_practica JOIN PRACTICA p ON d.id_practica = p.id_practica JOIN ESTUDIANTE e ON p.id_estudiante = e.id_estudiante JOIN JEFE_INMEDIATO j ON d.id_jefe_inmediato = j.id_jefe_inmediato JOIN CENTRO_PRACTICAS c ON j.id_centro_practicas = c.id_centro_practicas"
            )
            fichas = cursor.fetchall()

        conexion.commit()
    except psycopg2.Error as e:
        # Captura cualquier error y devuelve un mensaje de error como string
        conexion.rollback()
        fichas = f"Error al obtener fichas de desempeño: {e}"
    finally:
        # Cierra la conexión
        conexion.close()

    return fichas

def dar_baja_ficha_desempeno(p_id_ficha_desempeno, p_estado):
    try:
        conexion = obtener_conexion()

        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"

        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE ficha_desempeno SET estado = %s WHERE id_ficha_desempeno = %s",
                (new_estado, p_id_ficha_desempeno)
            )

        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        return f"Error al cambiar el estado de la ficha de desempeño: {str(e)}"

def consultar_ficha_desempeno(id_ficha_desempeno):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            # Obtener nombre y código universitario del estudiante
            cursor.execute("""
                SELECT e.nombre, e.cod_universitario
                FROM ESTUDIANTE e
                JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN FICHA_DESEMPENO fd ON dp.id_detalle_practica = fd.id_detalle_practica
                WHERE fd.id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato y cargo del jefe inmediato
            cursor.execute("""
                SELECT cp.razon_social, ji.nombre, ji.cargo
                FROM CENTRO_PRACTICAS cp
                JOIN JEFE_INMEDIATO ji ON cp.id_centro_practicas = ji.id_centro_practicas
                JOIN DETALLE_PRACTICA dp ON ji.id_jefe_inmediato = dp.id_jefe_inmediato
                JOIN FICHA_DESEMPENO fd ON dp.id_detalle_practica = fd.id_detalle_practica
                WHERE fd.id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            datos_cppp = cursor.fetchone()

            # Obtener información del detalle de práctica
            cursor.execute("""
                SELECT sa.nombre, dp.fecha_inicio, dp.fecha_fin
                FROM DETALLE_PRACTICA dp
                JOIN SEMESTRE_ACADEMICO sa ON dp.id_semestre_academico = sa.id_semestre
                JOIN FICHA_DESEMPENO fd ON dp.id_detalle_practica = fd.id_detalle_practica
                WHERE fd.id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            datos_practica = cursor.fetchone()

            # Obtener todos los registros de la tabla resultado_aprendizaje asociados a la ficha de desempeño
            cursor.execute("""
                SELECT *
                FROM RESULTADO_APRENDIZAJE
                WHERE id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            resultados_aprendizaje = cursor.fetchall()

            # Obtener el registro de la ficha de desempeño específica
            cursor.execute("""
            SELECT *
            FROM ficha_desempeno where id_ficha_desempeno=%s
            """, (id_ficha_desempeno,))
            ficha_desempeno = cursor.fetchone()

        conexion.close()

        return estudiante, datos_cppp, datos_practica, resultados_aprendizaje, ficha_desempeno

    except Exception as e:
        print(f"Error al consultar ficha de desempeño: {str(e)}")

