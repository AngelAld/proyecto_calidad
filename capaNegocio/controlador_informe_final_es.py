from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    informe_final_es = []
    conexion.close()
    return informe_final_es
