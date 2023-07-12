from capaDatos.bd import obtener_conexion
import capaNegocio.controlador_usuarios as controlador_usuarios
from datetime import datetime
import psycopg2
from psycopg2 import Error
from psycopg2.errors import UniqueViolation

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
                
                # controlador_usuarios.enviar_correo(contrasena=clave, nombres=nombre, usuario=cod_universitario, correo=correo_personal)
                # controlador_usuarios.enviar_correo(contrasena=clave, nombres=nombre, usuario=cod_universitario, correo=correo_usat)
               
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
        cursor.execute("DELETE FROM ")
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





def importar(registros):
    mensajes = []
    inserts = []
    try:
        conexion = obtener_conexion()
    except:
        return "Error al conectar a la base de datos"
    try:
        with conexion.cursor() as cursor:
            cursor.execute("select id_escuela_profesional, nombre from escuela_profesional where estado='A'")
            lista_escuelas = cursor.fetchall()
            cursor.execute("select id_plan_estudio, nombre, id_escuela_profesional from plan_estudio")
            lista_planes = cursor.fetchall()
            cursor.execute("select id_semestre, nombre from semestre_academico")
            lista_semestres = cursor.fetchall()
        conexion.close()
    except Exception as e:
        problema = "Error:" + repr(e).strip("'").replace("\\n", " ") 
        mensajes.append(['ERROR', 'ERROR', problema])

    for registro in registros:
        codigo_universitario = registro[0]
        nombre = registro[1]
        escuela_profesional = registro[2]
        dni = registro[3]
        correo_usat = registro[4]
        correo_personal = registro[5]
        telefono1 = registro[6]
        telefono2 = registro[7]
        semestre_ingreso = registro[8]
        plan_estudios = registro[9]
        
        problema = ""
        
        # Verificar si la escuela profesional existe en la lista
        escuela_encontrada = False
        id_escuela_profesional = None
        for escuela in lista_escuelas:
            if escuela[1] == escuela_profesional:
                escuela_encontrada = True
                id_escuela_profesional = escuela[0]
                break
        
        if not escuela_encontrada:
            problema = f"No existe la escuela: {escuela_profesional}"
            mensajes.append([codigo_universitario, nombre, problema])
            continue
        
        # Verificar si el DNI tiene 8 dígitos numéricos
        if not dni.isdigit() or len(dni) != 8:
            problema = "El DNI debe tener 8 dígitos numéricos"
            mensajes.append([codigo_universitario, nombre, problema])
            continue

        if  len(codigo_universitario) != 10:
            problema = "El Codigo universitario debe tener 10 caracteres"
            mensajes.append([codigo_universitario, nombre, problema])
            continue
        # Verificar si el correo USAT tiene el dominio correcto
        if not correo_usat.endswith("@usat.pe"):
            problema = "El correo USAT debe tener el dominio @usat.pe"
            mensajes.append([codigo_universitario, nombre, problema])
            continue
        
        # Verificar si el correo personal tiene el formato adecuado
        if "@" not in correo_personal or "." not in correo_personal:
            problema = "El correo personal debe contener al menos un '@' y un '.'"
            mensajes.append([codigo_universitario, nombre, problema])
            continue
        
        # Obtener el ID del plan de estudios
        id_plan_estudio = None
        for plan in lista_planes:
            if plan[1] == plan_estudios and plan[2] == id_escuela_profesional:
                id_plan_estudio = plan[0]
                break
        if id_plan_estudio is None:
            problema = "Plan de estudios no encontrado, se insertará el ultimo plan de estudios"
            mensajes.append([codigo_universitario, nombre, problema])
            id_plan_estudio = lista_planes[-1][0]
        
        # Obtener el ID del semestre de ingreso
        id_semestre_academico_ingreso = None
        for semestre in lista_semestres:
            if semestre[1] == semestre_ingreso:
                id_semestre_academico_ingreso = semestre[0]
                break
        if id_semestre_academico_ingreso is None:
            problema = "Semestre de ingreso no encontrado, se insertará el ultimo semestre"
            mensajes.append([codigo_universitario, nombre, problema])
            id_semestre_academico_ingreso = lista_semestres[-1][0]
        
        # Generar el comando INSERT INTO
        columnas_insert = [
            codigo_universitario,
            dni,
            nombre,
            correo_usat,
            correo_personal,
            telefono1,
            telefono2,
            'A',
            id_semestre_academico_ingreso,
            id_plan_estudio
        ]
        inserts.append(columnas_insert)
    return mensajes, inserts




import psycopg2
from psycopg2.errors import UniqueViolation

def insertar_importados(inserts):
    i = 0
    mensaje = ""
    problemas = []
    try:
        conexion = obtener_conexion()
    except:
        return "Error al conectar a la base de datos", []
    try:
        conexion.autocommit = False
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_rol FROM ROL WHERE nombre = 'Estudiante'")
            id_rol = cursor.fetchone()[0]
            estado = 'A'
            # Agregar punto de guardado antes de la iteración
            cursor.execute("SAVEPOINT start")
            for insert in inserts:
                codigo_universitario = insert[0]
                dni = insert[1]
                nombre = insert[2]
                correo_usat = insert[3]
                correo_personal = insert[4]
                telefono = insert[5]
                telefono2 = insert[6]
                id_semestre_academico_ingreso = insert[8]
                id_plan_estudio = insert[9]
                try:
                    # Agregar punto de guardado antes de cada inserción
                    cursor.execute("SAVEPOINT insert_estudiante")
                    cursor.execute(f"INSERT INTO ESTUDIANTE (cod_universitario, dni, nombre, correo_usat, correo_personal, telefono, telefono2, estado, id_semestre_academico_ingreso, id_plan_estudio) VALUES ('{codigo_universitario}', '{dni}', '{nombre}', '{correo_usat}', '{correo_personal}', '{telefono}', '{telefono2}', 'A', {id_semestre_academico_ingreso}, {id_plan_estudio});")
                    clave = ''.join([nombre[:3], codigo_universitario[:3]])
                    cursor.execute("SAVEPOINT insert_usuario")
                    cursor.execute("INSERT INTO USUARIO (usuario, nombre, clave, estado, id_rol) VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario", (codigo_universitario, nombre, controlador_usuarios.generate_password(clave), estado, id_rol))
                    id_usuario = cursor.fetchone()[0]
                    cursor.execute("UPDATE ESTUDIANTE SET id_usuario = %s WHERE cod_universitario = %s", (id_usuario, str(codigo_universitario)))
                    i += 1
                except UniqueViolation as e:
                    problema = f"Error al importar: Registro duplicado"
                    problemas.append([codigo_universitario, nombre, problema])
                    # Deshacer esta subtransacción y seguir con la siguiente
                    cursor.execute("ROLLBACK TO SAVEPOINT insert_estudiante")
                except Exception as e:
                    problema = "Error al importar: " + repr(e).strip("'").replace("\\n", " ")
                    problemas.append([codigo_universitario, nombre, problema])
                    # Deshacer esta subtransacción y seguir con la siguiente
                    cursor.execute("ROLLBACK TO SAVEPOINT insert_estudiante")
                # Agregar un punto de guardado después de cada inserción exitosa
                cursor.execute("SAVEPOINT after_insert")
            # Si todo va bien, hacer commit de la transacción
            conexion.commit()
            mensaje = f"Se importaron {i} estudiantes"
        conexion.close()
    except Exception as e:
        conexion.close()
        mensaje = "Error al importar: " + repr(e).strip("'").replace("\\n", " ")
        # Si algo falla, deshacer la transacción hasta el último punto de guardado
        cursor.execute("ROLLBACK TO SAVEPOINT start")
    finally:
        return mensaje, problemas

