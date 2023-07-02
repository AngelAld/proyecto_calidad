from capaDatos.bd import obtener_conexion

def listar_lineaDesarrollo():
    conexion = obtener_conexion()
    linea_desarrollo = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_linea_desarrollo()")
        linea_desarrollo = cursor.fetchall()
    conexion.close()
    return linea_desarrollo

#********************************************* Grafico de Barras *
    
def grafico_lineaDesarrollo():
    conexion = obtener_conexion()
    datos = []
    nombres_lineas = []
    
    with conexion.cursor() as cursor:
        # Obtener todas las líneas de desarrollo existentes
        cursor.execute("SELECT nombre FROM linea_desarrollo")
        lista_desarrollo = cursor.fetchall()
        
        for linea in lista_desarrollo:
            nombres_lineas.append(linea[0])  # Agregar el nombre de la línea a la lista de nombres
            
            # Obtener el conteo de estudiantes por línea de desarrollo
            cursor.execute("SELECT COUNT(DISTINCT es.nombre) FROM linea_desarrollo ld INNER JOIN detalle_practica dp ON dp.id_linea_desarrollo = ld.id_linea_desarrollo INNER JOIN practica pr ON pr.id_practica = dp.id_practica INNER JOIN estudiante es ON es.id_estudiante = pr.id_estudiante WHERE ld.nombre = %s", (linea[0],))
            conteo = cursor.fetchone()
            datos.append(conteo[0])
    # Imprimir los valores para verificar

    conexion.close()
    return datos, nombres_lineas
#***************************************************************


def agregar_lineaDesarrollo(nombre, descripcion, estado, id_escuelas):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_agregar_linea_desarrollo(%s, %s, %s, %s)",
            (nombre, descripcion, estado, id_escuelas),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def eliminar_lineaDesarrollo(id):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_eliminar_linea_desarrollo(%s)", (id,))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None


def buscar_lineaDesarrolloID(id):
    conexion = obtener_conexion()
    lineaDesarrollo = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select * from fn_consultar_linea_desarrollo_ID(%s)",
            (id,),
        )
        lineaDesarrollo = cursor.fetchone()
    conexion.close()
    return lineaDesarrollo


def actualizar_lineaDesarrollo(id, nombre, descripcion, estado, id_escuela):
    conexion = obtener_conexion()
    msg = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT fn_editar_linea_desarrollo(%s, %s, %s, %s, %s)",
            (id, nombre, descripcion, estado, id_escuela),
        )
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None

def dar_baja_lineaDesarrollo(id, estado):
    conexion = obtener_conexion()
    msg = []
    new_estado = ""
    if estado == "A":
        new_estado = "I"
    else:
        new_estado = "A"
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fn_actualizar_estado_linea_desarrollo(%s, %s)", (id, new_estado))
        msg = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return msg[0] if msg is not None else None



#********************************************* Lo uso para listar en combo a linea de desarrollo (NO BORRAR ESTA FUNCION) *
def obtener_escuelas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_escuela_profesional, nombre FROM ESCUELA_PROFESIONAL where estado='A'")
        escuelas = cursor.fetchall()
    conexion.close()
    return escuelas

#***************************************************************

#********************************************* Listar Escuelas y Facultades *
def obtener_facultades():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_facultad, nombre FROM FACULTAD")
        facultades = cursor.fetchall()
    conexion.close()
    return facultades

#***************************************************************

