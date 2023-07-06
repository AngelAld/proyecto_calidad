from capaDatos.bd import obtener_conexion

def listar_lineaDesarrollo():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    linea_desarrollo = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from fn_listar_linea_desarrollo()")
        linea_desarrollo = cursor.fetchall()
    conexion.close()
    return linea_desarrollo

#********************************************* Grafico de Barras *
    
def grafico_lineaDesarrollo():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    datos = []
    nombres_lineas = []
    try:
        with conexion.cursor() as cursor:
            # Obtener todas las líneas de desarrollo existentes
            cursor.execute("SELECT nombre FROM linea_desarrollo")
            lista_desarrollo = cursor.fetchall()
            
            for linea in lista_desarrollo:
                nombres_lineas.append(linea[0])  # Agregar el nombre de la línea a la lista de nombres
                
                # Obtener el conteo de estudiantes por línea de desarrollo
                cursor.execute("SELECT COUNT(DISTINCT es.nombre) FROM linea_desarrollo ld INNER JOIN detalle_practica dp ON dp.id_linea_desarrollo = ld.id_linea_desarrollo INNER JOIN practica pr ON pr.id_practica = dp.id_practica INNER JOIN estudiante es ON es.id_estudiante = pr.id_estudiante WHERE ld.nombre = %s LIMIT 1", (linea[0],))
                conteo = cursor.fetchone()
                datos.append(conteo[0])

        conexion.close()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al obtener los datos: " + str(e)
    finally:
        conexion.close()
    return datos, nombres_lineas


#******************************************************************************************************************************

def agregar_lineaDesarrollo(nombre, descripcion, estado, id_escuelas):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)
    
    msg = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_agregar_linea_desarrollo(%s, %s, %s, %s)",
                (nombre, descripcion, estado, id_escuelas),
            )
            msg = cursor.fetchone()
        conexion.commit()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al agregar línea de desarrollo: " + str(e)
    finally:
        conexion.close()
    
    return msg[0] if msg is not None else None

#******************************************************************************************************************************

def eliminar_lineaDesarrollo(id):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)
    
    try:
        msg = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT fn_eliminar_linea_desarrollo(%s)", (id,))
            msg = cursor.fetchone()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "No se pudo eliminar la línea de desarrollo: " + str(e)
    finally:
        conexion.commit()
        conexion.close()

    return msg[0] if msg is not None else None

#******************************************************************************************************************************

def buscar_lineaDesarrolloID(id):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    try:
        lineaDesarrollo = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "select * from fn_consultar_linea_desarrollo_ID(%s)",
                (id,),
            )
            lineaDesarrollo = cursor.fetchone()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al buscar la línea de desarrollo: " + str(e)
    finally:
        conexion.close()

    return lineaDesarrollo

#******************************************************************************************************************************

def actualizar_lineaDesarrollo(id, nombre, descripcion, estado, id_escuela):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    try:
        msg = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT fn_editar_linea_desarrollo(%s, %s, %s, %s, %s)",
                (id, nombre, descripcion, estado, id_escuela),
            )
            msg = cursor.fetchone()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al actualizar la línea de desarrollo: " + str(e)
    finally:
        conexion.commit()
        conexion.close()

    return msg[0] if msg is not None else None

#******************************************************************************************************************************

def dar_baja_lineaDesarrollo(id, estado):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    try:
        msg = []
        new_estado = ""
        if estado == "A":
            new_estado = "I"
        else:
            new_estado = "A"
        with conexion.cursor() as cursor:
            cursor.execute("SELECT fn_actualizar_estado_linea_desarrollo(%s, %s)", (id, new_estado))
            msg = cursor.fetchone()
    except Exception as e:
        conexion.rollback()  # Realizar rollback en caso de excepción
        return "Error al dar de baja la línea de desarrollo: " + str(e)
    finally:
        conexion.commit()
        conexion.close()

    return msg[0] if msg is not None else None

#********************************************* Lo uso para listar en combo a linea de desarrollo (NO BORRAR ESTA FUNCION) *
def obtener_escuelas():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)
    
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_escuela_profesional, nombre FROM ESCUELA_PROFESIONAL where estado='A'")
        escuelas = cursor.fetchall()
    conexion.close()
    return escuelas

#***************************************************************

#********************************************* Listar Semestre Academico  y Escuela para Reprote*
def listar_escuelas():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)
    
    with conexion.cursor() as cursor:
        cursor.execute("SELECT DISTINCT nombre FROM ESCUELA_PROFESIONAL where estado='A'")
        escuelas = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conexion.close()
    return escuelas


def listar_semestres():
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)
    
    with conexion.cursor() as cursor:
        cursor.execute("select DISTINCT nombre from semestre_academico")
        semestres = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conexion.close()
    return semestres
#***************************************************************

def graficar_porc_estudiante(semestre,escuela):
    try:
        conexion = obtener_conexion()
    except Exception as e:
        return "Error al conectar con la base de datos: " + str(e)

    datos = []
    semestre_lista = []
    escuela_lista = []
    
    # Obtener la lista de escuelas
    escuelas = listar_escuelas()
    escuela_lista.append(escuelas[0])  # Agregar la primera escuela a la lista de escuelas

    # Obtener la lista de semestres
    semestres = listar_semestres()
    semestre_lista.append(semestres[0])  # Agregar el primer semestre a la lista de semestres
    
    with conexion.cursor() as cursor:

    # Obtener el conteo de estudiantes por línea de desarrollo
        query_p = "select count( DISTINCT es.nombre) from estudiante es inner join practica pr on pr.id_estudiante = es.id_estudiante inner join semestre_academico sa on es.id_semestre_academico_ingreso = sa.id_semestre inner join plan_estudio pe on pe.id_plan_estudio = es.id_plan_estudio inner join escuela_profesional ep on ep.id_escuela_profesional = pe.id_escuela_profesional where pr.estado = 'P' AND ep.nombre = %s AND sa.nombre = %s"
        cursor.execute(query_p, (escuela, semestre))
        query_p_result = cursor.fetchone()
        datos.append(query_p_result[0] if query_p_result else 0)
      #  print(datos)
        query_f = "select count( DISTINCT es.nombre) from estudiante es inner join practica pr on pr.id_estudiante = es.id_estudiante inner join semestre_academico sa on es.id_semestre_academico_ingreso = sa.id_semestre inner join plan_estudio pe on pe.id_plan_estudio = es.id_plan_estudio inner join escuela_profesional ep on ep.id_escuela_profesional = pe.id_escuela_profesional where pr.estado = 'F' AND ep.nombre = %s AND sa.nombre = %s"
        cursor.execute(query_f, (escuela, semestre))
        query_f_result = cursor.fetchone()
        datos.append(query_f_result[0] if query_f_result else 0)
     #   print(datos)
    conexion.close()
    return datos, semestre_lista, escuela_lista