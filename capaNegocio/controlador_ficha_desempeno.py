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
                    DETALLE_PRACTICA.fecha_inicio AS fecha_inicio_practica,
                    DETALLE_PRACTICA.fecha_fin AS fecha_fin_practica
                FROM 
                    ESTUDIANTE
                JOIN 
                    PRACTICA ON ESTUDIANTE.id_estudiante = PRACTICA.id_estudiante
                JOIN 
                    DETALLE_PRACTICA ON PRACTICA.id_practica = DETALLE_PRACTICA.id_practica
                JOIN 
                    INFORME_INICIAL_ES ON DETALLE_PRACTICA.id_detalle_practica = INFORME_INICIAL_ES.id_detalle_practica
                JOIN 
                    INFORME_FINAL_ES ON DETALLE_PRACTICA.id_detalle_practica = INFORME_FINAL_ES.id_detalle_practica
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
                    CONCAT(u.num, ' ', u.via, ', ', u.ciudad) AS direccion,
                    ji.nombre AS nombre_responsable,
                    ji.correo AS correo_responsable
                FROM
                    FICHA_DESEMPENO fd
                JOIN
                    DETALLE_PRACTICA dp ON fd.id_detalle_practica = dp.id_detalle_practica
                JOIN
                    JEFE_INMEDIATO ji ON dp.id_jefe_inmediato = ji.id_jefe_inmediato
                JOIN
                    CENTRO_PRACTICAS cp ON ji.id_centro_practicas = cp.id_centro_practicas
                JOIN
                    UBICACION u ON cp.id_ubicacion = u.id_ubicacion
                JOIN
                    PRACTICA p ON dp.id_practica = p.id_practica
                WHERE
                    fd.id_ficha_desempeno = %s;
            """, (id_ficha_desempeno,))
            datos_cppp = cursor.fetchone()

            # Obtener información del detalle de práctica
            cursor.execute("""
                SELECT 
                    sa.nombre, 
                    dp.fecha_inicio, 
                    dp.fecha_fin,
                    ld.nombre AS area_desempeno
                FROM 
                    DETALLE_PRACTICA dp
                JOIN 
                    SEMESTRE_ACADEMICO sa ON dp.id_semestre_academico = sa.id_semestre
                JOIN 
                    FICHA_DESEMPENO fd ON dp.id_detalle_practica = fd.id_detalle_practica
                JOIN 
                    LINEA_DESARROLLO ld ON dp.id_linea_desarrollo = ld.id_linea_desarrollo
                WHERE 
                    fd.id_ficha_desempeno = %s
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
                FROM ficha_desempeno
                WHERE id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            ficha_desempeno = cursor.fetchone()

            # Obtener las conclusiones asociadas a la ficha de desempeño
            cursor.execute("""
                SELECT conclusiones
                FROM ficha_desempeno
                WHERE id_ficha_desempeno = %s
            """, (id_ficha_desempeno,))
            conclusiones = cursor.fetchone()[0] if cursor.rowcount > 0 else ""

        conexion.close()

        return estudiante, datos_cppp, datos_practica, resultados_aprendizaje, ficha_desempeno, conclusiones

    except Exception as e:
        print(f"Error al consultar ficha de desempeño: {str(e)}")


def actualizar_ficha_desempeno(id_ficha_desempeno,area_desempeno,conclusiones,responsabilidad,proactividad,comunicacion,trabajoequipo,compromiso,organizacion,puntualidad, firma_em, resultados_aprendizaje):
    try:
        conexion = obtener_conexion()
        conexion.autocommit = False

        
        with conexion.cursor() as cursor:
            sql_firmas = "UPDATE FICHA_DESEMPENO SET fecha = current_date"
            params_firmas = []
            
            if firma_em:
                sql_firmas += ", firma_em = %s"
                params_firmas.append(firma_em)

            sql_firmas += " WHERE id_ficha_desempeno = %s RETURNING id_detalle_practica"
            params_firmas.append(id_ficha_desempeno)
            
            cursor.execute(sql_firmas, params_firmas)
            
            cursor.execute("DELETE FROM RESULTADO_APRENDIZAJE WHERE id_ficha_desempeno = %s", (id_ficha_desempeno,))
            
            for resultado in resultados_aprendizaje:
                escala = resultado["escala"]
                descripcion = resultado["descripcion"]
                cursor.execute("INSERT INTO RESULTADO_APRENDIZAJE (escala, id_ficha_desempeno, descripcion) VALUES (%s, %s, %s)",
                               (escala, id_ficha_desempeno, descripcion))

            cursor.execute("UPDATE FICHA_DESEMPENO SET area_desemp=%s, responsabilidad = %s, proactividad = %s, comunicacion = %s, trabajo_equipo = %s, compromiso_calidad = %s, organizacion = %s, puntualidad = %s, firma_em = %s, conclusiones = %s WHERE id_ficha_desempeno = %s",
               (area_desempeno,responsabilidad, proactividad, comunicacion, trabajoequipo, compromiso, organizacion, puntualidad,firma_em, conclusiones, id_ficha_desempeno))


        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        conexion.rollback()
        return f"Error al actualizar informe: {str(e)}"



