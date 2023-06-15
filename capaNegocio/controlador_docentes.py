from capaDatos.bd import obtener_conexion

def listar_docentes():
    conexion = obtener_conexion()
    docentes = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("select * from fn_listar_docente_apoyo()")
    #     docentes = cursor.fetchall()
    conexion.close()
    return docentes

def agregar_docente(nombre, correo, id_titulo, id_escuela_profesional, id_usuario, estado):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_agregar_docente_apoyo(%s, %s, %s, %s, %s, %s)",
    #         (nombre, correo, id_titulo, id_escuela_profesional, id_usuario, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_docente(id):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_delete_docente(%s)", (id,))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_docenteID(id):
    conexion = obtener_conexion()
    docente = None
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT da.id_docente_apoyo, da.nombre, da.correo, ti.nombre, ep.nombre, us.usuario, da.estado FROM DOCENTE_APOYO da INNER JOIN titulo ti ON ti.id_titulo = da.id_titulo INNER JOIN escuela_profesional ep ON ep.id_escuela_profesional = da.id_escuela_profesional INNER JOIN usuario us ON us.id_usuario = us.id_usuario WHERE da.id_docente_apoyo=%s",
    #         (id,),
    #     )
    #     docente = cursor.fetchone()
    conexion.close()
    return docente

def actualizar_docente(id, nombre, correo, id_titulo, id_escuela_profesional, id_usuario, estado):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_update_semestre(%s, %s, %s, %s, %s, %s, %s)",
    #         (id, nombre, correo, id_titulo, id_escuela_profesional, id_usuario, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_docente(id, estado):
    conexion = obtener_conexion()
    msg = []
    # new_estado = ""
    # if estado == "A":
    #     new_estado = "I"
    # else:
    #     new_estado = "A"
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_update_estado(%s, %s)", (id, new_estado))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None