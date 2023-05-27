from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_semestres as c_semestres


semestres_bp = Blueprint("semestre", __name__, template_folder="templates")


@semestres_bp.route("/agregar_semestre")
def formulario_agregar_semestre():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_semestre.html")


@semestres_bp.route("/guardar_semestre", methods=["POST"])
def guardar_semestre():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        nombre = request.form["nombre"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        mensaje = c_semestres.insert(nombre, fecha_inicio, fecha_fin, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Semestre Registrado con Exito", "success")
            url = "/semestres"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_semestre"

        return redirect(url)


@semestres_bp.route("/semestres")
def semestres():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        semestres = c_semestres.getAll()
        return render_template("semestres.html", semestres=semestres)


@semestres_bp.route("/eliminar_semestre", methods=["POST"])
def eliminar_semestre():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_semestres.delete(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Semestre Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/semestres")


@semestres_bp.route("/formulario_editar_semestre/<int:id>")
def editar_semestre(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        semestre = c_semestres.getById(id)
        return render_template("frm_editar_semestre.html", semestre=semestre)


@semestres_bp.route("/actualizar_semestre", methods=["POST"])
def actualizar_semestre():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        nombre = request.form["nombre"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        mensaje = c_semestres.update(id, nombre, fecha_inicio, fecha_fin, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Semestre Actualizado con Exito", "success")
            url = "/semestres"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_semestre/" + id
        return redirect(url)


@semestres_bp.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_semestres.update_estado(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Semestre Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/semestres")
