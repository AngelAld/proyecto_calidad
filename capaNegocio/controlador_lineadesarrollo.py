from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    lineaDesarrollo = []
 #   with conexion.cursor() as cursor:
 #       cursor.execute("select * from fn_read_lineaDesarrollo()")
  #      lineaDesarrollo = cursor.fetchall()
    conexion.close()
    return lineaDesarrollo

def insert(nombre, descripcion, estado):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_create_lineaDesarrollo(%s, %s, %s)",
            (nombre, descripcion, estado),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None