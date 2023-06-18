from capaDatos.bd import obtener_conexion

def listar_practicas():
    conexion = obtener_conexion()
    practica = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("select * from fn_listar_practica()")
    #     practica = cursor.fetchall()
    conexion.close()
    return practica

def agregar_practica(nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_agregar_semestre(%s, %s, %s, %s)",
    #         (nombre, fecha_inicio, fecha_fin, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_practica(id):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_eliminar_semestre(%s)", (id,))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_practicaID(id):
    conexion = obtener_conexion()
    practica = None
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "select * from fn_consultar_semestre_academico_ID(%s)",
    #         (id,),
    #     )
    #     semestre = cursor.fetchone()
    conexion.close()
    return practica

def actualizar_practica(id, nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_editar_semestre(%s, %s, %s, %s, %s)",
    #         (id, nombre, fecha_inicio, fecha_fin, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_practica(id, estado):
    conexion = obtener_conexion()
    msg = []
    # new_estado = ""
    # if estado == "A":
    #     new_estado = "I"
    # else:
    #     new_estado = "A"
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_actualizar_estado_semestre(%s, %s)", (id, new_estado))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None