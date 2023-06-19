from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    ficha_desempeno = []
    conexion.close()
    return ficha_desempeno
