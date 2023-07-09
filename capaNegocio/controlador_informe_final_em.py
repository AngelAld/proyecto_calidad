from capaDatos.bd import obtener_conexion
import psycopg2

def listar_informes_final_empresa():
    conexion = obtener_conexion()
    informe_final_em = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas INFORME_INICIAL_ES, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT fin_em.id_informe_final_em, prac.razon_social, fin_em.estado FROM INFORME_FINAL_EM  fin_em INNER JOIN DETALLE_PRACTICA detalle_prac ON detalle_prac.id_detalle_practica= fin_em.id_detalle_practica INNER JOIN JEFE_INMEDIATO je_in ON  je_in.id_jefe_inmediato = detalle_prac.id_jefe_inmediato INNER JOIN CENTRO_PRACTICAS prac ON prac.id_centro_practicas=je_in.id_centro_practicas ORDER BY fin_em.estado, fin_em.id_informe_final_em ASC"
            )
            informe_final_em = cursor.fetchall()

        conexion.commit()
    except psycopg2.Error as e:
        # Captura cualquier error y devuelve un mensaje de error como string
        conexion.rollback()
        informe_final_em = f"Error al obtener informes: {e}"
    finally:
        # Cierra la conexión
        conexion.close()

    return informe_final_em

def consultar_informe_final_empresa(id_informe_final_em):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            # Obtener nombre del estudiante
            cursor.execute("""
                SELECT e.nombre, dp.fecha_inicio, dp.fecha_fin
                FROM ESTUDIANTE e
                JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN INFORME_FINAL_EM ife ON dp.id_detalle_practica = ife.id_detalle_practica
                WHERE ife.id_informe_final_em = %s
            """, (id_informe_final_em,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato, y cargo del jefe inmediato
            cursor.execute("""
                SELECT cp.razon_social, ji.nombre, ji.cargo
                FROM CENTRO_PRACTICAS cp
                JOIN JEFE_INMEDIATO ji ON cp.id_centro_practicas = ji.id_centro_practicas
                JOIN DETALLE_PRACTICA dp ON ji.id_jefe_inmediato = dp.id_jefe_inmediato
                JOIN INFORME_INICIAL_ES iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_es = %s
            """, (id_informe_final_em,))
            datos_cppp = cursor.fetchone()           
            
            cursor.execute("SELECT * FROM informe_final_em WHERE id_informe_final_em = %s", (id_informe_final_em,))
        conexion.close()

        return estudiante, datos_cppp

    except Exception as e:
        print("Error al consultar informe final empresa: {str(e)}")



def dar_baja_informe_final(p_id_informe_final_em, p_estado):
    try:
        conexion = obtener_conexion()

        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"

        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_actualizar_estado_informe_final_em(%s, %s)",
                (p_id_informe_final_em, new_estado),
            )

        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        return f"Error al cambiar el estado del informe: {str(e)}"
    

def eliminar_informe_final_em(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_informe_final_em(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_informe_final_em(id):
    conexion = obtener_conexion()
    planEstudio = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_editar_nombre_informe_final_em(%s)",
            (id,),
        )
        planEstudio = cursor.fetchone()
    conexion.close()
    return planEstudio