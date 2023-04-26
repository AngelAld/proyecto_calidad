from static.python.bd import obtener_conexion


def getAll():
    conexion = obtener_conexion()
    semestres = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_read_semestres()")
        semestres = cursor.fetchall()
    conexion.close()
    return semestres


def insert(nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_create_semestre(%s, %s, %s, %s)",
                       (nombre, fecha_inicio, fecha_fin, estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg


def delete(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_delete_semestre(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg


def getById(id):
    conexion = obtener_conexion()
    semestre = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_semestre, nombre, fecha_inicio, fecha_fin, estado FROM SEMESTRE_ACADEMICO WHERE id_semestre=%s", (id,))
        semestre = cursor.fetchone()
    conexion.close()
    return semestre


def update(id, nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_update_semestre(%s, %s, %s, %s, %s)",
                       (id, nombre, fecha_inicio, fecha_fin, estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg


def update_estado(id, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_update_estado(%s, %s)",
                       (id, estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg
