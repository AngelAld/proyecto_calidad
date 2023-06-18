from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    informe_inicial_em = []
    conexion.close()
    return informe_inicial_em
