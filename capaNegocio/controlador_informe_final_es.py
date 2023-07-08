from capaDatos.bd import obtener_conexion
import psycopg2

def listar_informes_finales_estudiante():
    conexion = obtener_conexion()
    informes = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas INFORME_FINAL_ES, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT i.id_informe_final_es, e.cod_universitario, e.nombre, c.alias, i.estado FROM informe_final_es i JOIN DETALLE_PRACTICA d ON i.id_detalle_practica = d.id_detalle_practica JOIN PRACTICA p ON d.id_practica = p.id_practica JOIN ESTUDIANTE e ON p.id_estudiante = e.id_estudiante JOIN JEFE_INMEDIATO j ON d.id_jefe_inmediato = j.id_jefe_inmediato JOIN CENTRO_PRACTICAS c ON j.id_centro_practicas = c.id_centro_practicas"
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

#########################################################################

def dar_baja_informe_final_estudiante(p_id_informe_final_estudiante, p_estado):
    try:
        conexion = obtener_conexion()

        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"

        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_actualizar_estado_informe_final_estudiante(%s, %s)",
                (p_id_informe_final_estudiante, new_estado),
            )

        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        return f"Error al cambiar el estado del informe final del estudiante: {str(e)}"


