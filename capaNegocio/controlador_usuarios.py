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
            check_password(row[3], password),
            row[4],
            row[5],
            row[6]
        ]
        print(list(row))
    return user


