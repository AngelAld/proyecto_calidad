from capaDatos.bd import obtener_conexion

def getAll():
     conexion = obtener_conexion()
     informe_inicial_es = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("select * from fn_read_semestres()")
    #     informe_inicial_es = cursor.fetchall()
     conexion.close()
     return informe_inicial_es