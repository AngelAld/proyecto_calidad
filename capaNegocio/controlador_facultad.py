from capaDatos.bd import obtener_conexion
def listar_facultades():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_facultad()")
        facultad = cursor.fetchall()
    conexion.close()
    return facultad


def agregar_facultad(nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_facultad(%s, %s, %s)",
             (nombre, descripcion, estado),
            )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_facultad(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_facultad(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_facultad(id):
    conexion = obtener_conexion()
    facultad = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_consultar_facultad_ID(%s)",
            (id,),
        )
        facultad = cursor.fetchone()
    conexion.close()
    return facultad


def actualizar_facultad(id, nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_facultad(%s, %s, %s, %s)",
            (id, nombre, descripcion,estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def dar_baja_facultad(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_facultad(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

#********************************************* Grafico de Barras *
    
def grafico_facultad():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    datos = []
    nombres_facultad = []
    try:
        with conexion.cursor() as cursor:
            # Obtener todas las líneas de desarrollo existentes
            cursor.execute("SELECT nombre FROM facultad")
            facultad = cursor.fetchall()
            
            for facu in facultad:
                nombres_facultad.append(facu[0])  # Agregar el nombre de la línea a la lista de nombres
                
                # Obtener el conteo de estudiantes por línea de desarrollo
                cursor.execute("SELECT COUNT(DISTINCT f.nombre) FROM facultad f INNER JOIN escuela_profesional ep ON f.id_facultad= ep.id_facultad INNER JOIN plan_estudio pe ON pe.id_escuela_profesional = ep.id_escuela_profesional INNER JOIN estudiante es ON es.id_plan_estudio =pe.id_escuela_profesional WHERE f.nombre =%s", (facu[0],))
                conteo = cursor.fetchone()
                datos.append(conteo[0])

        conexion.close()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al obtener los datos: " + str(e)
    finally:
        conexion.close()
    return datos, nombres_facultad


#******************************************************************************************************************************
