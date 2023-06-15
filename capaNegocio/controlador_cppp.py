from capaDatos import bd

def listar_cppp():
    conexion = bd.obtener_conexion()
    cpps = []
    with conexion.cursor() as cursor:
        cursor.execute()
        cpps = cursor.fetchall()
    conexion.close()
    return cpps

def obtener_cpppID(id_cppp):
    conexion = bd.obtener_conexion()
    cppp = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM cppp WHERE id_cppp = %s", (id_cppp,))
        cppp = cursor.fetchone()
    conexion.close()
    return cppp

def agregar_cpp(ruc, razon_social, rubro, telefono, correo, num, estado, tipo_via, via, lon, lat, ciudad, pais):
    conexion = bd.obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO cppp (ruc, razon_social, rubro, telefono, correo, num, estado, tipo_via, via, lon, lat, ciudad, pais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ruc, razon_social, rubro, telefono, correo, num, estado, tipo_via, via, lon, lat, ciudad, pais))
            msg = cursor.fetchone()
    conexion.commit()
    conexion.close()

