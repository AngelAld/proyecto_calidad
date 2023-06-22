from capaDatos.bd import obtener_conexion

def listar_jefe_inmediato():
    conexion = obtener_conexion()
    jefe_inmediato = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_jefe_inmediato()")
        jefe_inmediato = cursor.fetchall()
    conexion.close()
    return jefe_inmediato


def agregar_jefe_inmediato(nombre, correo, telefono, cargo, id_centro_practicas, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_jefe_inmediato(%s, %s, %s, %s, %s, %s)",
            (nombre, correo, telefono, cargo, id_centro_practicas, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_jefe_inmediato(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_jefe_inmediato(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_jefe_inmediatoID(id):
    conexion = obtener_conexion()
    Jefe_Inmediato = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select ji.id_jefe_inmediato, ji.nombre. ji.correo, ji.telefono, ji.cargo, cp.razon_social, ji.estado from JEFE_INMEDIATO ji INNER JOIN centro_practicas cp ON cp.id_centro_practicas = ji.id_centro_practicas WHERE ji.id_jefe_inmediato=%s",
            (id,),
        )
        Jefe_Inmediato = cursor.fetchone()
    conexion.close()
    return Jefe_Inmediato

def actualizar_jefe_inmediato(id, nombre, correo, telefono, cargo, id_centro_practicas, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_jefe_inmediato(%s, %s, %s, %s, %s, %s, %s)",
            (id, nombre, correo, telefono, cargo, id_centro_practicas, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_jefe_inmediato(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_jefe_inmediato(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

