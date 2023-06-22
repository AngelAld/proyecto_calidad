from capaDatos.bd import obtener_conexion

def listar_tituloProfesional():
    conexion = obtener_conexion()
    titulo_profesional = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_titulo_profesional()")
        titulo_profesional = cursor.fetchall()
    conexion.close()
    return titulo_profesional

def agregar_tituloProfesional(nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_titulo_profesional(%s, %s, %s)",
            (nombre, descripcion, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_tituloProfesional(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_titulo_profesional(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_tituloProfesionalID(id):
    conexion = obtener_conexion()
    titulo_profesional = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_titulo_profesional_ID(%s)",
            (id,),
        )
        titulo_profesional = cursor.fetchone()
    conexion.close()
    return titulo_profesional


def actualizar_tituloProfesional(id, nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_titulo_profesional(%s, %s, %s, %s)",
            (id, nombre, descripcion, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_tituloProfesional(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_titulo_profesional(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


