from capaDatos.bd import obtener_conexion

def listar_plan_estudio():
    conexion = obtener_conexion()
    planEstudio = []
    with conexion.cursor() as cursor:
       cursor.execute("select * from fn_listar_planEstudio()")
       planEstudio = cursor.fetchall()
    conexion.close()
    return planEstudio



def agregar_plan_estudio(nombre, estado, id_escuela_profesional):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_plan_estudio(%s, %s, %s)",
            (nombre, estado, id_escuela_profesional),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_plan_estudio(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_plan_estudio(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_plan_estudio_ID(id):
    conexion = obtener_conexion()
    planEstudio = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_plan_estudio_ID(%s)",
            (id,),
        )
        planEstudio = cursor.fetchone()
    conexion.close()
    return planEstudio

def actualizar_plan_estudio(id, nombre, estado, id_escuela_profesional):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_plan_estudio(%s, %s, %s, %s)",
            (id, nombre, estado, id_escuela_profesional),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_plan_estudio(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_plan_estudio(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None