from capaDatos.bd import obtener_conexion

def listar_lineaDesarrollo():
    conexion = obtener_conexion()
    linea_desarrollo = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_linea_desarrollo()")
        linea_desarrollo = cursor.fetchall()
    conexion.close()
    return linea_desarrollo


def agregar_lineaDesarrollo(nombre, descripcion, estado, id_escuelas):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_linea_desarrollo(%s, %s, %s, %s)",
            (nombre, descripcion, estado, id_escuelas),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_lineaDesarrollo(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_linea_desarrollo(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_lineaDesarrolloID(id):
    conexion = obtener_conexion()
    lineaDesarrollo = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_linea_desarrollo_ID(%s)",
            (id,),
        )
        lineaDesarrollo = cursor.fetchone()
    conexion.close()
    return lineaDesarrollo


def actualizar_lineaDesarrollo(id, nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_linea_desarrollo(%s, %s, %s, %s)",
            (id, nombre, descripcion, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_lineaDesarrollo(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_linea_desarrollo(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None



#********************************************* Lo uso para listar en combo a linea de desarrollo (NO BORRAR ESTA FUNCION) *
def obtener_escuelas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_escuela_profesional, nombre FROM ESCUELA_PROFESIONAL")
        escuelas = cursor.fetchall()
    conexion.close()
    return escuelas

#***************************************************************