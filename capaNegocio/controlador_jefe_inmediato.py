from capaDatos.bd import obtener_conexion
import capaNegocio.controlador_usuarios as controlador_usuarios

def listar_jefe_inmediato():
    conexion = obtener_conexion()
    jefe_inmediato = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_jefe_inmediato()")
        jefe_inmediato = cursor.fetchall()
    conexion.close()
    return jefe_inmediato


def agregar_jefe_inmediato(nombre, correo, telefono, cargo, estado, id_centro_practicas):
    conexion = obtener_conexion()
    msg = ""
    with conexion.cursor() as cursor:
        # Comprobar si el jefe inmediato ya existe
        cursor.execute("SELECT id_jefe_inmediato FROM JEFE_INMEDIATO WHERE nombre = %s OR correo = %s", (nombre, correo))
        resultado = cursor.fetchone()
        if resultado is not None:
            msg = "Jefe inmediato ya existe" if resultado[0] == nombre else "Correo ya registrado"
        else:
            try:
                # Obtener el id del rol "Jefe Inmediato"
                cursor.execute("SELECT id_rol FROM ROL WHERE nombre = 'Jefe Inmediato'")
                id_rol = cursor.fetchone()[0]
                # Insertar un nuevo usuario
                clave = ''.join([nombre[:3], correo[:3]])
                cursor.execute("INSERT INTO USUARIO (usuario, nombre, clave, estado, id_rol) VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario", (correo, nombre, controlador_usuarios.generate_password(clave), estado, id_rol))
                id_usuario = cursor.fetchone()[0]
                # Insertar un nuevo jefe inmediato
                cursor.execute("INSERT INTO JEFE_INMEDIATO (nombre, correo, telefono, cargo, estado, id_centro_practicas, id_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, correo, telefono, cargo, estado, id_centro_practicas, id_usuario))
                
                controlador_usuarios.enviar_correo(nombre, correo, clave, correo)
                
                msg = "Operación realizada con éxito"
                conexion.commit()
            except Exception as e:
                msg = str(e)
                conexion.rollback()

    conexion.close()
    return msg

def eliminar_jefe_inmediato(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_jefe_inmediato(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def buscar_jefe_inmediatoID(id):
    conexion = obtener_conexion()
    Jefe_Inmediato = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_jefe_inmediato_ID(%s)",
            # "select ji.id_jefe_inmediato, ji.nombre. ji.correo, ji.telefono, ji.cargo, cp.razon_social, ji.estado from JEFE_INMEDIATO ji INNER JOIN centro_practicas cp ON cp.id_centro_practicas = ji.id_centro_practicas WHERE ji.id_jefe_inmediato=%s",
            (id,),
        )
        Jefe_Inmediato = cursor.fetchone()
    conexion.close()
    return Jefe_Inmediato

def actualizar_jefe_inmediato(id, nombre, correo, telefono, cargo, estado, id_centro_practicas):
    conexion = obtener_conexion()
    msg = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT * from fn_editar_jefe_inmediato(%s, %s, %s, %s, %s, %s, %s)",
                (id, nombre, correo, telefono, cargo, estado, id_centro_practicas),
            )
            msg = cursor.fetchone()
        conexion.commit()
    except Exception as e:
        print(f"Error al ejecutar la consulta SQL: {str(e)}")
    finally:
        conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_jefe_inmediato(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_jefe_inmediato(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

#********************************************* Listar Centro de practicas *
def obtener_centro_practicas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_centro_practicas, razon_social FROM CENTRO_PRACTICAS")
        centro_PPP = cursor.fetchall() #verificar si está así
    conexion.close()
    return centro_PPP #verificar si está así
##
#***************************************************************