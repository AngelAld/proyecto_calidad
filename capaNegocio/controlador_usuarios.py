from capaDatos.bd import obtener_conexion
from werkzeug.security import check_password_hash


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


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
            row[3],
            check_password(row[4], password),
            row[5],
            row[6],
            row[7],
        ]
    return user
