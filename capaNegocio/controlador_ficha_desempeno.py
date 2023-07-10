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
                SELECT 
                ESTUDIANTE.nombre AS nombre_estudiante,
                ESCUELA_PROFESIONAL.nombre AS nombre_escuela_profesional,
                INFORME_INICIAL_EM.fecha AS fecha_inicio_practica,
                INFORME_FINAL_EM.fecha AS fecha_fin_practica
                FROM 
                ESTUDIANTE
                JOIN 
                PRACTICA ON ESTUDIANTE.id_estudiante = PRACTICA.id_estudiante
                JOIN 
                DETALLE_PRACTICA ON PRACTICA.id_practica = DETALLE_PRACTICA.id_practica
                JOIN 
                INFORME_INICIAL_EM ON DETALLE_PRACTICA.id_detalle_practica = INFORME_INICIAL_EM.id_detalle_practica
                JOIN 
                INFORME_FINAL_EM ON DETALLE_PRACTICA.id_detalle_practica = INFORME_FINAL_EM.id_detalle_practica
                JOIN 
                ESCUELA_PROFESIONAL ON ESTUDIANTE.id_plan_estudio = ESCUELA_PROFESIONAL.id_escuela_profesional
                WHERE 
                ESTUDIANTE.id_estudiante = %s;
            """, (id_ficha_desempeno,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato y cargo del jefe inmediato
            cursor.execute("""
                SELECT
                cp.razon_social,
                u.num || ' ' || u.via || ', ' || u.ciudad AS direccion,
                ji.nombre AS nombre_responsable,
                ji.correo AS correo_responsable
                FROM
                ESTUDIANTE e
                JOIN
                PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN
                DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN
                JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato
                JOIN
                CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas
                JOIN
                UBICACION u ON cp.id_ubicacion = u.id_ubicacion
                WHERE
                e.id_estudiante = %s;
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

def actualizar_informe_inicial(id_ficha_desempeno, firma_em,responsabilidad, proactividad, comunicacion, trabajo_equipo,compromiso_calidad,organizacion,puntualidad,fecha,area_desempeno):
    try:
        conexion = obtener_conexion()
        conexion.autocommit = False
        print(firma_em)
        with conexion.cursor() as cursor:
            sql_firmas = "UPDATE FICHA_DESEMPENO SET fecha = current_date"
            params_firmas = []
            if firma_em:
                sql_firmas += ", firma_em = %s"
                params_firmas.append(firma_em)

            sql_firmas += " WHERE id_ficha_desempeno = %s RETURNING id_detalle_practica"
            params_firmas.append(id_ficha_desempeno)

            cursor.execute(sql_firmas, params_firmas)

            id_detalle_practica = cursor.fetchone()[0]

            if fecha:
                sql = "UPDATE DETALLE_PRACTICA SET "
                params = []

                if fecha:
                    sql += "fecha = %s, "
                    params.append(fecha)

                sql = sql[:-2] + " WHERE id_detalle_practica = %s"
                params.append(id_detalle_practica)

                cursor.execute(sql, params)
            
            cursor.execute("DELETE FROM OBJETIVO WHERE id_informe_inicial_es = %s", (id_informe_inicial_es,))

            for descripcion in descripciones:
                cursor.execute("INSERT INTO OBJETIVO (id_informe_inicial_es, descripcion) VALUES (%s, %s)", (id_informe_inicial_es, descripcion))

            cursor.execute("DELETE FROM PLAN_TRABAJO WHERE id_informe_inicial_es = %s", (id_informe_inicial_es,))

            for trabajo in plan_trabajo:
                cursor.execute("INSERT INTO PLAN_TRABAJO (id_informe_inicial_es, n_semana, fecha_inicio, fecha_fin, actividad, num_horas) VALUES (%s, %s, %s, %s, %s, %s)", (id_informe_inicial_es, trabajo["n_semana"], trabajo["fecha_inicio"], trabajo["fecha_fin"], trabajo["actividad"], trabajo["horas"]))

        conexion.commit()
        conexion.close()

        return "Operacion realizada con éxito"

    except Exception as e:
        conexion.rollback()
        return f"Error al actualizar informe: {str(e)}"

