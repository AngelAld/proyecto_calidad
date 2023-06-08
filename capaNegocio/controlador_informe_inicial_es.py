from capaDatos.bd import obtener_conexion


def getAll():
    # conexion = obtener_conexion()
    # informe_inicial_es = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("select * from fn_read_semestres()")
    #     informe_inicial_es = cursor.fetchall()
    #     conexion.close()
    return informe_inicial_es


def insert(nombre, fecha_inicio, fecha_fin, estado):
    # conexion = obtener_conexion()
    # msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_create_semestre(%s, %s, %s, %s)",
    #         (nombre, fecha_inicio, fecha_fin, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    # conexion.close()
    return msg[0] if msg is not None else None


def delete(id):
    # conexion = obtener_conexion()
    # msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_delete_semestre(%s)", (id,))
    #     msg = cursor.fetchone()
    # conexion.commit()
    # conexion.close()
    return msg[0] if msg is not None else None


def getById(id):
    # conexion = obtener_conexion()
    # informe_inicial_es = None
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT id_semestre, nombre, fecha_inicio, fecha_fin, estado FROM SEMESTRE_ACADEMICO WHERE id_semestre=%s",
    #         (id,),
    #     )
    #     informe_inicial_es = cursor.fetchone()
    # conexion.close()
    return informe_inicial_es


def update(id, nombre, fecha_inicio, fecha_fin, estado):
    # conexion = obtener_conexion()
    # msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_update_semestre(%s, %s, %s, %s, %s)",
    #         (id, nombre, fecha_inicio, fecha_fin, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    # conexion.close()
    return msg[0] if msg is not None else None


def update_estado(id, estado):
    # conexion = obtener_conexion()
    # msg = []
    # new_estado = ""
    # if estado == "A":
    #     new_estado = "I"
    # else:
    #     new_estado = "A"
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_update_estado(%s, %s)", (id, new_estado))
    #     msg = cursor.fetchone()
    # conexion.commit()
    # conexion.close()
    return msg[0] if msg is not None else None
