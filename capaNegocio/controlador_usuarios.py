from capaDatos.bd import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash

@classmethod
def check_password(self, hashed_password, password):
    return check_password_hash(hashed_password, password)



def login():
    conexion = obtener_conexion()
    user = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_login()")
        user = cursor.fetchall()
    conexion.close()
    return user
