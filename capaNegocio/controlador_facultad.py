from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    facultades = []
    #with conexion.cursor() as cursor:
        #cursor.execute("select * from fn_read_semestres()")
       # semestres = cursor.fetchall()
    conexion.close()
    return facultades
