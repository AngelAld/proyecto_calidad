from capaDatos import bd
from capaDatos.bd import obtener_conexion

def listar_cppp():
    conexion = bd.obtener_conexion()
    cpps = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_centro_practica()")
        cpps = cursor.fetchall()
    conexion.close()
    return cpps

def actualizar_centroPPP(id, ruc, razon_social, alias, rubro, telefono, correo):
    if id_ubicacion == "":
        id_ubicacion = "-"
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_centro_practicas(%s, %s, %s, %s, %s, %s, %s)",
            (id, ruc, razon_social, alias, rubro, telefono, correo),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_CentroPPPID(id):
    conexion = obtener_conexion()
    centroPPP = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_centroPPP_ID(%s)",
            (id,),
        )
        centroPPP = cursor.fetchone()
    conexion.close()
    return centroPPP

def obtener_cpppID(id_cppp):
    conexion = bd.obtener_conexion()
    cppp = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cppp WHERE id_cppp = %s", (id_cppp,))
        cppp = cursor.fetchone()
    conexion.close()
    return cppp

def agregar_centroPPP(ruc, razon_social, alias, rubro, telefono, correo):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_centro_practicas(%s, %s, %s, %s, %s, %s)",
            (ruc, razon_social, alias, rubro, telefono, correo),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def eliminar_centroPPP(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_centro_practicas(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_CPPP(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_centro_practicas(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None