from capaDatos import bd
from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    centroPractica = []
 #   with conexion.cursor() as cursor:
 #       cursor.execute("select * from fn_read_lineaDesarrollo()")
  #      lineaDesarrollo = cursor.fetchall()
    conexion.close()
    return centroPractica

def listar_cppp():
    conexion = bd.obtener_conexion()
    cpps = []
    with conexion.cursor() as cursor:
        cursor.execute()
        cpps = cursor.fetchall()
    conexion.close()
    return cpps

def actualizar_centroPPP(id, ruc, razon_social, alias, rubro, telefono, correo, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_centro_practicas(%s, %s, %s, %s, %s, %s, %s, %s)",
            (id, ruc, razon_social, alias, rubro, telefono, correo, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_cpppID(id_cppp):
    conexion = bd.obtener_conexion()
    cppp = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cppp WHERE id_cppp = %s", (id_cppp,))
        cppp = cursor.fetchone()
    conexion.close()
    return cppp

def agregar_centroPPP(ruc, razon_social, alias, rubro, telefono, correo, id_ubicacion):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_centro_practicas(%s, %s, %s, %s, %s, %s, %s)",
            (ruc, razon_social, alias, rubro, telefono, correo, id_ubicacion),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

