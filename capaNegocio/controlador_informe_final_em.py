from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    informe_final_em = []
    conexion.close()
    return informe_final_em
