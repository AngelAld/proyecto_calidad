from capaDatos.bd import obtener_conexion

def listar_practicas():
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_practicas()")
        practica = cursor.fetchall()
    conexion.close()
    return practica

def agregar_practica(id_estudiante, estado, id_linea_desarrollo, fecha_inicio, fecha_fin, id_semestre_academico, horas, id_jefe_inmediato, informacion_adicional):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_agregar_practica(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id_estudiante, estado, id_linea_desarrollo, fecha_inicio, fecha_fin, id_semestre_academico, horas, id_jefe_inmediato, informacion_adicional),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None



def eliminar_practica(id):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_eliminar_semestre(%s)", (id,))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_practicaID(id):
    conexion = obtener_conexion()
    practica = None
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "select * from fn_consultar_semestre_academico_ID(%s)",
    #         (id,),
    #     )
    #     semestre = cursor.fetchone()
    conexion.close()
    return practica

def actualizar_practica(id, nombre, fecha_inicio, fecha_fin, estado):
    conexion = obtener_conexion()
    msg = []
    # with conexion.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT fn_editar_semestre(%s, %s, %s, %s, %s)",
    #         (id, nombre, fecha_inicio, fecha_fin, estado),
    #     )
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_practica(id, estado):
    conexion = obtener_conexion()
    msg = []
    # new_estado = ""
    # if estado == "A":
    #     new_estado = "I"
    # else:
    #     new_estado = "A"
    # with conexion.cursor() as cursor:
    #     cursor.execute("SELECT fn_actualizar_estado_semestre(%s, %s)", (id, new_estado))
    #     msg = cursor.fetchone()
    # conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_estudiantes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_estudiante, nombre FROM ESTUDIANTE")
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante

def obtener_centro_practicas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_centro_practicas, alias FROM CENTRO_PRACTICAS")
        centro_practicas = cursor.fetchall()
    conexion.close()
    return centro_practicas

def obtener_jefe_inmediato():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_jefe_inmediato, nombre FROM JEFE_INMEDIATO")
        jefeInmediato = cursor.fetchall()
    conexion.close()
    return jefeInmediato

def obtener_semestre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_semestre, nombre FROM SEMESTRE_ACADEMICO")
        semestre_academico = cursor.fetchall()
    conexion.close()
    return semestre_academico

def obtener_lineaDesarrollo():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_linea_desarrollo, nombre FROM LINEA_DESARROLLO")
        lineaDesarrollo = cursor.fetchall()
    conexion.close()
    return lineaDesarrollo