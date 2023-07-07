from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_practica as c_practica


practica_bp = Blueprint("practica", __name__, template_folder="templates")


@practica_bp.route("/agregar_practica")
def formulario_agregar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiantes, centro_practicas, jefeInmediatos, semestre_academicos, lineaDesarrollos = c_practica.obtener_datos_agregar()
        # estudiantes = c_practica.obtener_estudiantes()
        # centro_practicas = c_practica.obtener_centro_practicas()
        # jefeInmediatos=c_practica.obtener_jefe_inmediato()
        # semestre_academicos=c_practica.obtener_semestre()
        # lineaDesarrollos=c_practica.obtener_lineaDesarrollo()
        return render_template("frm_agregar_practica.html",estudiantes=estudiantes,centro_practicas=centro_practicas,jefeInmediatos=jefeInmediatos,semestre_academicos=semestre_academicos,lineaDesarrollos=lineaDesarrollos)


@practica_bp.route("/guardar_practica", methods=["POST"])
def guardar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_estudiante = int(request.form["estudiante"])
        estado = request.form["estado"]
        id_linea_desarrollo = request.form["lineaDesarrollo"]
        id_semestre_academico = request.form["semestreAcademico"]
        id_jefe_inmediato = request.form["jefeInmediato"]
        informacion_adicional = request.form["informacionAdicional"]
    try:
        mensaje = c_practica.agregar_practica(
            id_estudiante, estado, id_linea_desarrollo, id_semestre_academico, id_jefe_inmediato,
            informacion_adicional
        )

        flash("Práctica registrada con éxito", "success")
        url = "/practicas"
    except ValueError as e:
        mensaje = str(e)
        flash("Error al registrar la práctica: " + mensaje, "error")
        url = "/agregar_practica"

    return redirect(url)
    

@practica_bp.route("/practicas")
def practicas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            practicas = c_practica.listar_practicas()
            if isinstance(practicas,list):
                return render_template("practica.html", practicas=practicas)
            else:
                print(str(practicas))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener practicas: {e}")
            return redirect(url_for("inicio.inicio"))


@practica_bp.route("/eliminar_practica", methods=["POST"])
def eliminar_practica_route():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_practica.eliminar_practica(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Práctica eliminada con éxito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/practicas")
    
@practica_bp.route("/eliminar_detalle_practica", methods=["POST"])
def eliminar_detalle_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        data = request.get_json()
        detalle_id = data['id']
        deleted = c_practica.eliminar_detalle_practica(detalle_id)
        print('Si esta entrando')
        if deleted:
            flash(f"Práctica eliminada con éxito", "success")
        else:
            flash("Error al eliminar la práctica", "error")

        return redirect("/practicas")

@practica_bp.route("/formulario_editar_practica/<int:id>")
def editar_practica(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        practica = c_practica.buscar_practica_por_ID(id)
        if practica == []:
            c_practica.eliminar_practica(id)
            flash("Se eliminaron todos los detalles de esta practica pre profesional", "warning")
            return redirect("/practicas")
        centro_practicas, jefeInmediatos, semestre_academicos, lineaDesarrollos = c_practica.obtener_datos_editar()
        # centro_practicas = c_practica.obtener_centro_practicas()
        # if centro_practicas == []:
        #     flash("No se encontraron centros de practica", "error")
        #     return redirect("/practicas")
        # jefeInmediatos = c_practica.obtener_jefe_inmediato()
        # if jefeInmediatos == []:
        #     flash("No se encontraron Jefes inmediatos", "error")
        #     return redirect("/practicas")
        # semestre_academicos = c_practica.obtener_semestre()
        # if semestre_academicos == []:
        #     flash("No se encontraron Semestres Académicos", "error")
        #     return redirect("/practicas")
        # lineaDesarrollos = c_practica.obtener_lineaDesarrollo()
        # if lineaDesarrollos == []:
        #     flash("No se encontraron lineas de desarrollo", "error")
        #     return redirect("/practicas")
        return render_template("frm_editar_practica.html", detallesPracticas=practica, centro_practicas=centro_practicas, jefeInmediatos=jefeInmediatos, semestre_academicos=semestre_academicos, lineaDesarrollos=lineaDesarrollos)



@practica_bp.route("/actualizar_practica", methods=["POST"])
def actualizar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_d_practica = request.form.get("id")
        estado = request.form.get("estado")
        id_linea_desarrollo = request.form.get("lineaDesarrollo")
        id_semestre_academico = request.form.get("semestreAcademico")
        id_jefe_inmediato = request.form.get("jefeInmediato")
        informacion_adicional = request.form.get("informacionAdicional")

        mensaje = c_practica.actualizar_practica(id_d_practica, id_linea_desarrollo, id_jefe_inmediato, informacion_adicional, estado, id_semestre_academico)

        if mensaje == "Operación realizada con éxito":
            flash("Práctica actualizada con éxito", "success")
            url = "/practicas"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_practica/" + str(id_practica)
        return redirect(url)


@practica_bp.route("/actualizar_estado_practica", methods=["POST"])
def actualizar_estado_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_practica.dar_baja_practica(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Práctica Actualizada con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/practicas")
    

@practica_bp.route("/reporte_practica1")
def formulario_reporte_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            datos,nombres_meses = c_practica.grafico_meses_practica('2023-01-01','2024-07-07')
            print(nombres_meses)
            return render_template("reporte_practica.html", datos=datos, nombres_meses=nombres_meses)   
        except Exception as e:
            flash(str(e), "error")
            return redirect("/practicas")
        
@practica_bp.route("/reporte_practica2")
def formulario_reporte_practica2():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            datos, nombre_estados = c_practica.grafico_estado_practica('2023-01-01', '2023-07-07')
            return render_template("reporte_practica2.html", datos=datos, nombres_estados=nombre_estados)
        except Exception as e:
            flash(str(e), "error")
            return redirect("/practicas")
        