from capaDatos.bd import obtener_conexion
import capaNegocio.controlador_usuarios as controlador_usuarios

def listar_docentes():
    conexion = obtener_conexion()
    docentes = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_docente_apoyo()")
        docentes = cursor.fetchall()
    conexion.close()
    return docentes

def agregar_docente(nombre, correo, estado, id_titulo, id_escuela_profesional):
    conexion = obtener_conexion()
    msg = ""
    with conexion.cursor() as cursor:
        # Comprobar si el docente ya existe
        cursor.execute("SELECT id_docente_apoyo FROM DOCENTE_APOYO WHERE nombre = %s OR correo = %s", (nombre, correo))
        resultado = cursor.fetchone()
        if resultado is not None:
            msg = "Docente de apoyo ya existe" if resultado[0] == nombre else "Correo ya registrado"
        else:
            try:
                # Obtener el id del rol "Docente de Apoyo"
                cursor.execute("SELECT id_rol FROM ROL WHERE nombre = 'Docente de Apoyo'")
                id_rol = cursor.fetchone()[0]
                # Insertar un nuevo usuario
                clave = ''.join([nombre[:3], correo[:3]])
                cursor.execute("INSERT INTO USUARIO (usuario, nombre, clave, estado, id_rol) VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario", (correo, nombre, controlador_usuarios.generate_password(clave), estado, id_rol))
                id_usuario = cursor.fetchone()[0]
                # Insertar un nuevo docente de apoyo
                cursor.execute("INSERT INTO DOCENTE_APOYO (nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario))
                
                controlador_usuarios.enviar_correo(nombre, correo, clave, correo)
                
                msg = "Operación realizada con éxito"
                conexion.commit()
            except Exception as e:
                msg = str(e)
                conexion.rollback()

    conexion.close()
    return msg

def eliminar_docente(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_docente_apoyo(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_docenteID(id):
    conexion = obtener_conexion()
    docente = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM fn_consultar_docente_apoyo_id(%s)",
            (id,),
        )
        docente = cursor.fetchone()
    conexion.close()
    return docente

def actualizar_docente(id, nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_docente_apoyo(%s, %s, %s, %s, %s, %s, %s)",
            (id, nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def actualizar_estado_docente(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_docente_apoyo(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def obtener_titulo():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_titulo, nombre FROM TITULO_PROFESIONAL")
        titulo = cursor.fetchall()
    conexion.close()
    return titulo

def obtener_escuela_profesional():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_escuela_profesional, nombre FROM ESCUELA_PROFESIONAL")
        escuelaprofesional = cursor.fetchall()
    conexion.close()
    return escuelaprofesional

