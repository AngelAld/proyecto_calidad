from capaDatos.bd import obtener_conexion


def getAll():
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_estudiante()")
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante


def insert(cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_estudiante(%s, %s, %s, %s , %s,%s, %s, %s, %s, %s , %s)",
            (cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def delete(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_estudiante(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def getById(id):
    conexion = obtener_conexion()
    semestre = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_estudiante_id(%s)",
            (id,),
        )
        semestre = cursor.fetchone()
    conexion.close()
    return semestre


def update(id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_estudiante(%s, %s, %s, %s, %s , %s,%s, %s, %s, %s, %s , %s)",
            (id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def update_estado(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_estudiante(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_planestudio():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_plan_estudio, nombre FROM PLAN_ESTUDIO")
        planestudio = cursor.fetchall()
    conexion.close()
    return planestudio

def obtener_semesteacademico():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_semestre, nombre FROM semestre_academico")
        semesteacademico = cursor.fetchall()
    conexion.close()
    return semesteacademico

def obtener_usuario():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_usuario,usuario from usuario")
        usuario = cursor.fetchall()
    conexion.close()
    return usuario