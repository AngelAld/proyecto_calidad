from capaDatos.bd import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash
import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def generate_password(password):
    return generate_password_hash(password)

def login(username, password):
    conexion = obtener_conexion()
    user = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_login(%s)", (username, ),
        )
        row = cursor.fetchone()
    conexion.close()
    if row == None:
        return None
    else:
        user = [
            row[0],
            row[1],
            row[2],
            check_password(row[3], password),
            row[4],
            row[5],
            row[6]
        ]
        print(list(row))
    return user

def enviar_correo(nombres, usuario, contrasena, correo):
    # Configurar la información del correo electrónico
    remitente = 'aaaldana50@gmail.com' # Cambiar al correo que se utilizará para enviar el mensaje
    destinatario = correo
    asunto = 'Credenciales del sistema de practicas'

    # Configurar el texto del mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    texto = f'''Estimado {nombres},

Se ha generado su cuenta para Practicas Pre Profesionales

usuario    : {usuario}
contraseña : {contrasena}

Ingrese a usatpracticas.xyz para acceder. 

El staff de EduTech.'''
    mensaje.attach(MIMEText(texto))

    # Enviar el mensaje
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login('aaaldana50@gmail.com', 'gkvyprjtacdqxbkb') # Cambiar al correo y contraseña de aplicación que se utilizará para enviar el mensaje
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        print('Correo electrónico enviado con éxito')
    except Exception as e:
        print(f'Error al enviar el correo electrónico: {e}')


def actualizar_contrasena(id_usuario, contrasena_actual, nueva_contrasena):
    conexion = obtener_conexion()
    msg = []

    try:
        with conexion.cursor() as cursor:
            # Verificar la contraseña actual del usuario
            cursor.execute("SELECT clave FROM usuario WHERE id_usuario = %s", (id_usuario,))
            resultado = cursor.fetchone()
            if resultado is None:
                print("Usuario no encontrado.")
                return
            clave_actual = resultado[0]

            # Comparar la contraseña actual ingresada con la registrada en la base de datos
            if not check_password(clave_actual, contrasena_actual):
                print("La contraseña actual ingresada no coincide.")
                return

            # Actualizar la contraseña del usuario
            gener_nueva_contrasena = generate_password(nueva_contrasena)
            cursor.execute("UPDATE usuario SET clave = %s WHERE id_usuario = %s", (gener_nueva_contrasena, id_usuario))
            msg = cursor.fetchone()

        # Confirmar los cambios en la base de datos
        conexion.commit()
        print("Contraseña actualizada con éxito.")
    except (Exception, psycopg2.Error) as error:
        print("Error al actualizar la contraseña:", error)
    finally:
        if conexion:
            conexion.close()

    return msg[0] if msg is not None else None
