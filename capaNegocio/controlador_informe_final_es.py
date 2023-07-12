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

def dar_baja_informe_final_estudiante(p_id_informe_final_es, p_estado):
    try:
        conexion = obtener_conexion()
        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_actualizar_estado_informe_final_estudiante(%s, %s)",
                (p_id_informe_final_es, new_estado),
            )
        conexion.commit()
        conexion.close()
        return "Operación realizada con éxito"
    except Exception as e:
        return f"Error al cambiar el estado del informe final del estudiante: {str(e)}"
    
    
def consultar_informe_finales_estudiante(id_informe_final_es):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            # Obtener nombre y código universitario del estudiante
            cursor.execute("""
                SELECT e.nombre AS nombre_estudiante, ep.nombre AS nombre_escuela_profesional
                FROM ESTUDIANTE e
                JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN INFORME_FINAL_ES ife ON dp.id_detalle_practica = ife.id_detalle_practica
                JOIN PLAN_ESTUDIO pe ON e.id_plan_estudio = pe.id_plan_estudio
                JOIN ESCUELA_PROFESIONAL ep ON pe.id_escuela_profesional = ep.id_escuela_profesional
                WHERE ife.id_informe_final_es = %s;
            """, (id_informe_final_es,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato, y cargo del jefe inmediato
            cursor.execute("""
                SELECT cp.razon_social, u.ciudad, cp.rubro, cp.alias, ji.nombre AS representante_legal
                FROM CENTRO_PRACTICAS cp
                JOIN UBICACION u ON cp.id_ubicacion = u.id_ubicacion
                JOIN PRACTICA p ON cp.id_centro_practicas = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN INFORME_FINAL_ES ife ON dp.id_detalle_practica = ife.id_detalle_practica
                JOIN JEFE_INMEDIATO ji ON cp.id_centro_practicas = ji.id_centro_practicas
                WHERE ife.id_informe_final_es = %s;
            """, (id_informe_final_es,))
            datos_cppp = cursor.fetchone()

            # Obtener información del detalle de práctica
            cursor.execute("""
                SELECT sa.nombre, dp.fecha_inicio, dp.fecha_fin
                FROM DETALLE_PRACTICA dp
                JOIN SEMESTRE_ACADEMICO sa ON dp.id_semestre_academico = sa.id_semestre
                JOIN INFORME_INICIAL_ES iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_es = %s
            """, (id_informe_final_es,))
            datos_practica = cursor.fetchone()

            # Obtener todos los registros de la tabla objetivo asociados al informe inicial
            cursor.execute("""
                SELECT *
                FROM OBJETIVO
                WHERE id_informe_inicial_es = %s
            """, (id_informe_final_es,))
            objetivos = cursor.fetchall()

            # Obtener todos los registros de la tabla plan_trabajo asociados al informe inicial
            cursor.execute("""
                SELECT *
                FROM PLAN_TRABAJO
                WHERE id_informe_inicial_es = %s
            """, (id_informe_final_es,))
            plan_trabajo = cursor.fetchall()

            cursor.execute("SELECT * FROM informe_inicial_es WHERE id_informe_inicial_es = %s", (id_informe_final_es,))
            informe = cursor.fetchone()
        conexion.close()

        return estudiante, datos_cppp, datos_practica, objetivos, plan_trabajo, informe

    except Exception as e:
        print(f"Error al consultar informe inicial: {str(e)}")


