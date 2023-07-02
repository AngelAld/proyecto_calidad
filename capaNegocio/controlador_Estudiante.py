from capaDatos.bd import obtener_conexion
import capaNegocio.controlador_usuarios as controlador_usuarios

def getAll():
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_estudiante()")
        estudiante = cursor.fetchall()
    conexion.close()
    return estudiante


def insert(cod_universitario, dni, nombre, correo_usat, correo_personal, telefono, telefono2, estado, id_semestre_academico_ingreso, id_plan_estudio):
    conexion = obtener_conexion()
    msg = ""
    with conexion.cursor() as cursor:
        # Comprobar si el estudiante ya existe
        cursor.execute("SELECT id_estudiante FROM ESTUDIANTE WHERE cod_universitario = %s OR dni = %s", (cod_universitario, dni))
        resultado = cursor.fetchone()
        if resultado is not None:
            msg = "Estudiante ya existe en la base de datos"
        else:
            try:
                # Obtener el id del rol "Estudiante"
                cursor.execute("SELECT id_rol FROM ROL WHERE nombre = 'Estudiante'")
                id_rol = cursor.fetchone()[0]
                # Insertar un nuevo usuario
                clave = ''.join([nombre[:3], cod_universitario[:3]])
                cursor.execute("INSERT INTO USUARIO (usuario, nombre, clave, estado, id_rol) VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario", (cod_universitario, nombre, controlador_usuarios.generate_password(clave), estado, id_rol))
                id_usuario = cursor.fetchone()[0]
                # Insertar un nuevo estudiante
                cursor.execute("INSERT INTO ESTUDIANTE (cod_universitario, dni, nombre, correo_usat, correo_personal, telefono, telefono2, estado, id_usuario, id_semestre_academico_ingreso, id_plan_estudio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (cod_universitario, dni, nombre, correo_usat, correo_personal, telefono, telefono2, estado, id_usuario, id_semestre_academico_ingreso, id_plan_estudio))
                
                controlador_usuarios.enviar_correo(contrasena=clave, nombres=nombre, usuario=cod_universitario, correo=correo_personal)
                
                msg = "Operación realizada con éxito"
                conexion.commit()
            except Exception as e:
                msg = str(e)
                conexion.rollback()

    conexion.close()
    return msg


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


def update(id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_semestre_academico_ingreso,id_plan_estudio):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_estudiante(%s, %s, %s, %s, %s , %s,%s, %s, %s, %s, %s )",
            (id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_semestre_academico_ingreso,id_plan_estudio),
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
        cursor.execute("SELECT id_plan_estudio, nombre FROM PLAN_ESTUDIO where estado='A'")
        planestudio = cursor.fetchall()
    conexion.close()
    return planestudio

def obtener_semesteacademico():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_semestre, nombre FROM semestre_academico where estado='A'")
        semesteacademico = cursor.fetchall()
    conexion.close()
    return semesteacademico

def obtener_usuario():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_usuario,usuario from usuario where estado='A'")
        usuario = cursor.fetchall()
    conexion.close()
    return usuario