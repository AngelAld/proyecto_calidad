from capaDatos.bd import obtener_conexion

def getAll():
    conexion = obtener_conexion()
    escuelas = []
    #with conexion.cursor() as cursor:
        #cursor.execute("select * from fn_read_semestres()")
       # semestres = cursor.fetchall()
    conexion.close()
    return escuelas
