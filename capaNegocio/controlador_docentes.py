from capaDatos.bd import obtener_conexion

def listar_docentes():
    conexion = obtener_conexion()
    docentes = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_docente_apoyo()")
        docentes = cursor.fetchall()
    conexion.close()
    return docentes

def agregar_docente(nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_docente_apoyo(%s, %s, %s, %s, %s, %s)",
            (nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_docente(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_delete_docente(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_docenteID(id):
    conexion = obtener_conexion()
    docente = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_consultar_docente_apoyo_ID(%s)",
            (id,),
        )
        docente = cursor.fetchone()
    conexion.close()
    return docente

def actualizar_docente(id, nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_update_semestre(%s, %s, %s, %s, %s, %s, %s)",
            (id, nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_docente(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_update_estado(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_titulos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_titulo, nombre FROM TITULO_PROFESIONAL where estado='A'")
        escuelas = cursor.fetchall()
    conexion.close()
    return escuelas

def obtener_escuelas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_escuela_profesional, nombre FROM ESCUELA_PROFESIONAL where estado='A'")
        escuelas = cursor.fetchall()
    conexion.close()
    return escuelas