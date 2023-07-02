from capaDatos import bd
from capaDatos.bd import obtener_conexion

def listar_cppp():
    conexion = bd.obtener_conexion()
    cpps = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_centro_practica()")
        cpps = cursor.fetchall()
    conexion.close()
    return cpps

def actualizar_centroPPP(id, ruc, razon_social, alias, rubro, telefono, correo):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * from fn_editar_centro_practicas(%s, %s, %s, %s, %s, %s, %s)",
            (id, ruc, razon_social, alias, rubro, telefono, correo),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_CentroPPPID(id):
    conexion = obtener_conexion()
    centroPPP = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_centroPPP_ID(%s)",
            (id,),
        )
        centroPPP = cursor.fetchone()
    conexion.close()
    return centroPPP

def obtener_cpppID(id_cppp):
    conexion = bd.obtener_conexion()
    cppp = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cppp WHERE id_cppp = %s", (id_cppp,))
        cppp = cursor.fetchone()
    conexion.close()
    return cppp

def agregar_centroPPP(ruc, razon_social, alias, rubro, telefono, correo):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_centro_practicas(%s, %s, %s, %s, %s, %s)",
            (ruc, razon_social, alias, rubro, telefono, correo),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_centroPPP(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_centro_practicas(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_CPPP(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_centro_practicas(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def agregar_ubicacion(id_centro_practicas, num, via, lon, lat, pais, ciudad, estado):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    msg = ""
    with conexion.cursor() as cursor:
        try:
            # Registrar una nueva ubicación
            cursor.execute("INSERT INTO UBICACION (num, via, lon, lat, pais, ciudad, estado) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_ubicacion", (num, via, lon, lat, pais, ciudad, estado))
            id_ubicacion = cursor.fetchone()[0]
            # Agregar id_ubicacion a un centro de prácticas
            cursor.execute("UPDATE CENTRO_PRACTICAS SET id_ubicacion = %s WHERE id_centro_practicas = %s", (id_ubicacion, id_centro_practicas))
            # Realizar commit y devolver mensaje de éxito
            msg = "Operación realizada con éxito"
            conexion.commit()
        except Exception as e:
            # Realizar rollback en caso de falla y devolver mensaje de error
            msg = str(e)
            conexion.rollback()
    
    # Cerrar la conexión y devolver el mensaje
    conexion.close()
    return msg

def actualizar_ubicacion(id_ubicacion, num, via, lon, lat, pais, ciudad, estado):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    msg = ""
    with conexion.cursor() as cursor:
        try:
            # Actualizar una ubicación existente
            cursor.execute("UPDATE UBICACION SET num = %s, via = %s, lon = %s, lat = %s, pais = %s, ciudad = %s, estado = %s WHERE id_ubicacion = %s", (num, via, lon, lat, pais, ciudad, estado, id_ubicacion))
            # Realizar commit y devolver mensaje de éxito
            msg = "Operación realizada con éxito"
            conexion.commit()
        except Exception as e:
            # Realizar rollback en caso de falla y devolver mensaje de error
            msg = str(e)
            conexion.rollback()

    # Cerrar la conexión y devolver el mensaje
    conexion.close()
    return msg

def obtener_ubicacion_por_id(id_ubicacion):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    with conexion.cursor() as cursor:
        try:
            # Obtener una ubicación por ID
            cursor.execute("SELECT * FROM UBICACION WHERE id_ubicacion = %s", (id_ubicacion,))
            ubicacion = cursor.fetchone()
            # Devolver la ubicación
            return ubicacion
        except Exception as e:
            # Realizar rollback en caso de falla y devolver mensaje de error
            conexion.rollback()
            return "Error al obtener la ubicación: " + str(e)
    
    # Cerrar la conexión
    conexion.close()