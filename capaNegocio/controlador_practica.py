from capaDatos.bd import obtener_conexion
import psycopg2

def listar_practicas():
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_practicas()")
        practica = cursor.fetchall()
    conexion.close()
    return practica

def agregar_practica(id_estudiante, estado, id_linea_desarrollo, id_semestre_academico, id_jefe_inmediato, informacion_adicional):
    conexion = obtener_conexion()
    msg = ""
    try:
        with conexion.cursor() as cursor:
            # Inicia la transacción
            conexion.autocommit = False

            # Verifica si ya existe una práctica para el estudiante
            cursor.execute("SELECT id_practica FROM PRACTICA WHERE id_estudiante = %s", (id_estudiante,))
            practica_existente = cursor.fetchone()

            if practica_existente:
                id_practica = practica_existente[0]
            else:
                # Registra una nueva práctica y obtiene el ID generado
                cursor.execute("INSERT INTO PRACTICA (id_estudiante, estado) VALUES (%s,'P') RETURNING id_practica", (id_estudiante,))
                id_practica = cursor.fetchone()[0]
            # Registra un nuevo detalle de práctica
            cursor.execute("INSERT INTO DETALLE_PRACTICA (informacion_adicional, estado, id_practica, id_jefe_inmediato, id_semestre_academico, id_linea_desarrollo) VALUES (%s, %s, %s, %s, %s, %s)",
                           (informacion_adicional, estado, id_practica, id_jefe_inmediato, id_semestre_academico, id_linea_desarrollo))

            # Confirma la transacción
            conexion.commit()
            msg = "La práctica se registró correctamente."

    except psycopg2.Error as e:
        # Realiza un rollback en caso de error y captura el mensaje de error
        conexion.rollback()
        msg = f"Error al registrar la práctica: {e}"

    finally:
        # Restaura la conexión a su configuración predeterminada y cierra la conexións
        conexion.close()

    return msg


def eliminar_practica(id):
    conexion = obtener_conexion()
    msg = None  # Cambiar [] por None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_practica(%s)", (id,))
        msg = cursor.fetchone() # Obtener el primer elemento del resultado
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_detalle_practica(id):
    try:
        conexion = obtener_conexion()
        conexion.autocommit = False
        with conexion.cursor() as cursor:
            # Elimina los datos directamente en lugar de usar una función SQL
            cursor.execute("DELETE FROM detalle_practica WHERE id_detalle_practica = %s", (id,))
        conexion.commit()
        msg = "Operación realizada con éxito"
    except Exception as e:
        conexion.rollback()
        msg = str(e)       
    finally:
        conexion.close()
    return msg

def buscar_practica_por_ID(id_practica):
    conexion = obtener_conexion()
    practica = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_consultar_practica_por_ID(%s)",
            (id_practica,),
        )
        practica = cursor.fetchall()
    conexion.close()
    return practica



def actualizar_practica(id_detalle_practica, id_linea_desarrollo, id_jefe_inmediato, informacion_adicional, estado, id_semestre_academico):
    try:   
        conexion = obtener_conexion()
        conexion.autocommit = False 
        with conexion.cursor() as cursor:  
            # Actualiza los campos relevantes directamente          
            cursor.execute("""
                UPDATE detalle_practica
                SET id_linea_desarrollo = %s,
                    id_jefe_inmediato = %s,
                    informacion_adicional = %s,
                    estado = %s,
                    id_semestre_academico = %s   
                WHERE id_detalle_practica = %s""",
                (id_linea_desarrollo,
                 id_jefe_inmediato, 
                 informacion_adicional, 
                 estado,
                 id_semestre_academico,
                 id_detalle_practica))           
        conexion.commit()       
        msg = "Operación realizada con éxito"         
    except Exception as e:
        conexion.rollback()
        msg = str(e)
    finally:      
        conexion.close()
    return msg


def dar_baja_practica(id_practica, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "P":
        new_estado = "F"
    else:
        new_estado = "P"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_practica(%s, %s)", (id_practica, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_estudiantes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_estudiante, nombre FROM ESTUDIANTE")
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante

def obtener_centro_practicas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_centro_practicas, alias FROM CENTRO_PRACTICAS")
        centro_practicas = cursor.fetchall()
    conexion.close()
    return centro_practicas

def obtener_jefe_inmediato():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_jefe_inmediato, nombre, id_centro_practicas FROM JEFE_INMEDIATO")
        jefeInmediato = cursor.fetchall()
    conexion.close()
    return jefeInmediato

def obtener_semestre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_semestre, nombre FROM SEMESTRE_ACADEMICO")
        semestre_academico = cursor.fetchall()
    conexion.close()
    return semestre_academico

def obtener_lineaDesarrollo():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_linea_desarrollo, nombre FROM LINEA_DESARROLLO")
        lineaDesarrollo = cursor.fetchall()
    conexion.close()
    return lineaDesarrollo

#--------------------------------------------------------------------#
def grafico_estudiantes():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    datos = []

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT nombre FROM linea_desarrollo")
            lista_desarrollo = cursor.fetchall()

            for linea in lista_desarrollo:
                cursor.execute("""
                    SELECT COUNT(DISTINCT es.nombre)
                    FROM linea_desarrollo ld
                    INNER JOIN detalle_practica dp ON dp.id_linea_desarrollo = ld.id_linea_desarrollo
                    INNER JOIN practica pr ON pr.id_practica = dp.id_practica
                    INNER JOIN estudiante es ON es.id_estudiante = pr.id_estudiante
                    WHERE ld.nombre = %s
                    AND EXTRACT(YEAR FROM pr.fecha_inicio) <= 2023
                    AND EXTRACT(YEAR FROM pr.fecha_fin) >= 2023
                """, (linea[0],))

                conteo = cursor.fetchone()
                datos.append((conteo[0], linea[0]))

    except Exception as e:
        conexion.rollback()
        return "Error al obtener los datos: " + str(e)

    finally:
        conexion.close()

    return datos