from capaDatos.bd import obtener_conexion
import psycopg2


def listar_informes_iniciales_estudiante():
    conexion = obtener_conexion()
    informes = []
    try:
        with conexion.cursor() as cursor:
            # Obtiene la información requerida de las tablas INFORME_INICIAL_ES, DETALLE_PRACTICA, ESTUDIANTE y CENTRO_PRACTICAS
            cursor.execute(
                "SELECT i.id_informe_inicial_es, e.cod_universitario, e.nombre, c.alias, i.estado FROM informe_inicial_es i JOIN DETALLE_PRACTICA d ON i.id_detalle_practica = d.id_detalle_practica JOIN PRACTICA p ON d.id_practica = p.id_practica JOIN ESTUDIANTE e ON p.id_estudiante = e.id_estudiante JOIN JEFE_INMEDIATO j ON d.id_jefe_inmediato = j.id_jefe_inmediato JOIN CENTRO_PRACTICAS c ON j.id_centro_practicas = c.id_centro_practicas"
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


def consultar_informe_iniciales_estudiante(id_informe_inicial_es):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            # Obtener nombre y código universitario del estudiante
            cursor.execute("""
                SELECT e.nombre, e.cod_universitario
                FROM ESTUDIANTE e
                JOIN PRACTICA p ON e.id_estudiante = p.id_estudiante
                JOIN DETALLE_PRACTICA dp ON p.id_practica = dp.id_practica
                JOIN INFORME_INICIAL_ES iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_es = %s
            """, (id_informe_inicial_es,))
            estudiante = cursor.fetchone()

            # Obtener información del centro de prácticas, jefe inmediato, y cargo del jefe inmediato
            cursor.execute("""
                SELECT cp.razon_social, ji.nombre, ji.cargo
                FROM CENTRO_PRACTICAS cp
                JOIN JEFE_INMEDIATO ji ON cp.id_centro_practicas = ji.id_centro_practicas
                JOIN DETALLE_PRACTICA dp ON ji.id_jefe_inmediato = dp.id_jefe_inmediato
                JOIN INFORME_INICIAL_ES iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_es = %s
            """, (id_informe_inicial_es,))
            datos_cppp = cursor.fetchone()

            # Obtener información del detalle de práctica
            cursor.execute("""
                SELECT sa.nombre, dp.fecha_inicio, dp.fecha_fin
                FROM DETALLE_PRACTICA dp
                JOIN SEMESTRE_ACADEMICO sa ON dp.id_semestre_academico = sa.id_semestre
                JOIN INFORME_INICIAL_ES iie ON dp.id_detalle_practica = iie.id_detalle_practica
                WHERE iie.id_informe_inicial_es = %s
            """, (id_informe_inicial_es,))
            datos_practica = cursor.fetchone()

            # Obtener todos los registros de la tabla objetivo asociados al informe inicial
            cursor.execute("""
                SELECT *
                FROM OBJETIVO
                WHERE id_informe_inicial_es = %s
            """, (id_informe_inicial_es,))
            objetivos = cursor.fetchall()

            # Obtener todos los registros de la tabla plan_trabajo asociados al informe inicial
            cursor.execute("""
                SELECT *
                FROM PLAN_TRABAJO
                WHERE id_informe_inicial_es = %s
            """, (id_informe_inicial_es,))
            plan_trabajo = cursor.fetchall()
            
            cursor.execute("SELECT * FROM informe_inicial_es WHERE id_informe_inicial_es = %s", (id_informe_inicial_es,))
            informe = cursor.fetchone()
        conexion.close()

        return estudiante, datos_cppp, datos_practica, objetivos, plan_trabajo, informe

    except Exception as e:
        print("Error al consultar informe inicial: {str(e)}")




def dar_baja_informe_inicial(p_id_informe_inicial_es, p_estado):
    try:
        conexion = obtener_conexion()

        if p_estado == "P":
            new_estado = "A"
        else:
            new_estado = "P"

        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_actualizar_estado_informe_inicial_es(%s, %s)",
                (p_id_informe_inicial_es, new_estado),
            )

        conexion.commit()
        conexion.close()

        return "Operación realizada con éxito"

    except Exception as e:
        return f"Error al cambiar el estado del informe: {str(e)}"



# ********************************************* Lo uso para listar los datos de estudiante*



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


def actualizar_informe_inicial(id_informe_inicial_es, totalHoras, firma_es, firma_jefe, descripciones, fecha_inicio, fecha_fin, plan_trabajo):
    try:
        conexion = obtener_conexion()
        conexion.autocommit = False
        print(firma_es)
        print(firma_jefe)
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE INFORME_INICIAL_ES SET fecha = current_date, firma_es = %s, firma_jefe = %s WHERE id_informe_inicial_es = %s RETURNING id_detalle_practica", (firma_es, firma_jefe, id_informe_inicial_es))

            id_detalle_practica = cursor.fetchone()[0]

            if fecha_inicio or fecha_fin or totalHoras:
                sql = "UPDATE DETALLE_PRACTICA SET "
                params = []

                if fecha_inicio:
                    sql += "fecha_inicio = %s, "
                    params.append(fecha_inicio)

                if fecha_fin:
                    sql += "fecha_fin = %s, "
                    params.append(fecha_fin)

                if totalHoras:
                    params.append(totalHoras)
                    sql += "horas = %s, "

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