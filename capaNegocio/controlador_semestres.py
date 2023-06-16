from capaDatos.bd import obtener_conexion


def listar_semestres():
    conexion = obtener_conexion()
    semestres = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_semestre_academico()")
        semestres = cursor.fetchall()
    conexion.close()
    return semestres


def agregar_semestre(nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_semestre(%s, %s, %s, %s)",
            (nombre, fecha_inicio, fecha_fin, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_semestre(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_semestre(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_semestreID(id):
    conexion = obtener_conexion()
    semestre = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_semestre_academico_ID(%s)",
            (id,),
        )
        semestre = cursor.fetchone()
    conexion.close()
    return semestre


def actualizar_semestre(id, nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_semestre(%s, %s, %s, %s, %s)",
            (id, nombre, fecha_inicio, fecha_fin, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def dar_baja_semestre(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_semestre(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None
