from capaDatos.bd import obtener_conexion
def listar_facultades():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_facultad()")
        facultad = cursor.fetchall()
    conexion.close()
    return facultad

def cargar_facultades():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("select f.nombre from facultad f")
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