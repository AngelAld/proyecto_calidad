from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_practica as c_practica


practica_bp = Blueprint("practica", __name__, template_folder="templates")


@practica_bp.route("/agregar_practica")
def formulario_agregar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiantes = c_practica.obtener_estudiantes()
        centro_practicas = c_practica.obtener_centro_practicas()
        jefeInmediatos=c_practica.obtener_jefe_inmediato()
        semestre_academicos=c_practica.obtener_semestre()
        lineaDesarrollos=c_practica.obtener_lineaDesarrollo()
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
        practicas = c_practica.listar_practicas()
        return render_template("practica.html", practicas=practicas)


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
        detalle_id = request.form["id"]
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
        centro_practicas = c_practica.obtener_centro_practicas()
        jefeInmediatos = c_practica.obtener_jefe_inmediato()
        semestre_academicos = c_practica.obtener_semestre()
        lineaDesarrollos = c_practica.obtener_lineaDesarrollo()
        print((practica))
        return render_template("frm_editar_practica.html", detallesPracticas=practica, centro_practicas=centro_practicas, jefeInmediatos=jefeInmediatos, semestre_academicos=semestre_academicos, lineaDesarrollos=lineaDesarrollos)



@practica_bp.route("/actualizar_practica", methods=["POST"])
def actualizar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_practica = request.form.get("id")
        id_estudiante = request.form.get("estudiante")  # Corregido aquí
        estado = request.form.get("estado")
        id_linea_desarrollo = request.form.get("lineaDesarrollo")
        fecha_inicio = request.form.get("fechaInicio")
        fecha_fin = request.form.get("fechaFin")
        id_semestre_academico = request.form.get("semestreAcademico")
        horas = request.form.get("horas")
        id_jefe_inmediato = request.form.get("jefeInmediato")
        informacion_adicional = request.form.get("informacionAdicional")

        mensaje = c_practica.actualizar_practica(id_estudiante, estado, id_linea_desarrollo, fecha_inicio, fecha_fin, id_semestre_academico, horas, id_jefe_inmediato, informacion_adicional)

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
    

@practica_bp.route("/reporte_practica")
def formulario_reporte_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        datos = c_practica.grafico_estudiantes()
        return render_template("reporte_practica.html", datos=datos)