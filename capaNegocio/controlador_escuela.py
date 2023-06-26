from capaDatos.bd import obtener_conexion
def listar_facultades():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_facultad()")
        facultad = cursor.fetchall()
    conexion.close()
    return facultad

def listar_escuela():
    conexion = obtener_conexion()
    escuela = []
    with conexion.cursor() as cursor:
        cursor.execute("select e.id_escuela_profesional, e.nombre, e.descripcion,e.estado, f.nombre from escuela_profesional e inner join facultad f on e.id_facultad= f.id_facultad")
        #cursor.execute("select * from fn_listar_escuela_profesional()")
        escuela = cursor.fetchall()
    conexion.close()
    return escuela


def agregar_escuela(nombre, descripcion, estado, id_facultad):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_escuela_profesional(%s, %s, %s, %s)",
             (nombre, descripcion, estado,id_facultad),
            )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_escuela(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_escuela_profesional(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_escuela(id):
    conexion = obtener_conexion()
    escuela = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_consultar_escuela_profesional_id(%s)",
            (id,),
        )
        escuela = cursor.fetchone()
    conexion.close()
    return escuela


def actualizar_escuela(id, nombre, descripcion, estado,id_facultad):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_escuela_profesional(%s, %s, %s, %s, %s )",
            (id, nombre, descripcion,estado,id_facultad),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def dar_baja_escuela(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_escuela(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

#********************************************* Lo uso para listar facultades en combo a escuela (NO BORRAR ESTA FUNCION) *
def cargar_facultades():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("select id_facultad, nombre from facultad where estado='A'")
        facultad = cursor.fetchall()
    conexion.close()
    return facultad

#***************************************************************