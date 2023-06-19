from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_Estudiante as c_estudiante


estudiante_bp = Blueprint("estudiante", __name__, template_folder="templates")


@estudiante_bp.route("/agregar_estudiante")
def formulario_agregar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_estudiante.html")


@estudiante_bp.route("/guardar_estudiante", methods=["POST"])
def guardar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        cod_universitario = request.form["cod_universitario"]
        dni = request.form["dni"]
        nombre = request.form["nombre"]
        correo_usat = request.form["correo_usat"]
        correo_personal = request.form["correo_personal"]
        telefono = request.form["telefono"]
        telefono2 = request.form["telefono2"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_usuario = request.form["id_usuario"]
        id_semestre_academico_ingreso = request.form["id_semestre_academico_ingreso"]
        id_plan_estudio = request.form["id_plan_estudio"]

        mensaje = c_estudiante.insert(cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio)

        if mensaje == "Operación realizada con éxito":
            flash(f"estudiante Registrado con Exito", "success")
            url = "/estudiante"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_estudiante"

        return redirect(url)


@estudiante_bp.route("/estudiante")
def estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiante = c_estudiante.getAll()
        return render_template("estudiante.html", estudiante=estudiante)


@estudiante_bp.route("/eliminar_estudiante", methods=["POST"])
def eliminar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_estudiante.delete(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"estudiante Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/estudiante")


@estudiante_bp.route("/formulario_editar_estudiante/<int:id>")
def editar_estudiante(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiante = c_estudiante.getById(id)
        return render_template("frm_editar_estudiante.html", estudiante=estudiante)


@estudiante_bp.route("/actualizar_estudiante", methods=["POST"])
def actualizar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        cod_universitario = request.form["cod_universitario"]
        dni = request.form["dni"]
        nombre = request.form["nombre"]
        correo_usat = request.form["correo_usat"]
        correo_personal = request.form["correo_personal"]
        telefono = request.form["telefono"]
        telefono2 = request.form["telefono2"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_usuario = request.form["id_usuario"]
        id_semestre_academico_ingreso = request.form["id_semestre_academico_ingreso"]
        id_plan_estudio = request.form["id_plan_estudio"]
        
        mensaje = c_estudiante.update(id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_usuario,id_semestre_academico_ingreso,id_plan_estudio)

        if mensaje == "Operación realizada con éxito":
            flash(f"estudiante Actualizado con Exito", "success")
            url = "/estudiante"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_estudiante/" + id
        return redirect(url)


@estudiante_bp.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_estudiante.update_estado(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"estudiante Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/estudiante")
