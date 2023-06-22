from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_tituloProfesional as c_tituloProfesional


titulo_profesional_bp = Blueprint("tituloProfesional", __name__, template_folder="templates")

@titulo_profesional_bp.route("/titulo_profesional")
def titulo_profesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        titulo_profesional = c_tituloProfesional.listar_tituloProfesional()
        return render_template("tituloProfesional.html", titulo_profesional=titulo_profesional)


@titulo_profesional_bp.route("/agregar_tituloProfesional")
def formulario_agregar_tituloProfesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_tituloProfesional.html")


@titulo_profesional_bp.route("/guardar_tituloProfesional", methods=["POST"])
def guardar_tituloProfesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
       
        mensaje = c_tituloProfesional.agregar_tituloProfesional(nombre, descripcion, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Titulo Profesional Registrada con Exito", "success")
            url = "/titulo_profesional"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_tituloProfesional"
            
        return redirect(url)


@titulo_profesional_bp.route("/eliminar_tituloProfesional", methods=["POST"])
def eliminar_tituloProfesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_tituloProfesional.eliminar_tituloProfesional(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Titulo Profesional Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect("/titulo_profesional")


@titulo_profesional_bp.route("/formulario_editar_tituloProfesional/<int:id>")
def editar_tituloProfesional(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        tituloProfesional = c_tituloProfesional.buscar_tituloProfesionalID(id)
        return render_template("frm_editar_tituloProfesional.html", tituloProfesional=tituloProfesional)


@titulo_profesional_bp.route("/actualizar_tituloProfesional", methods=["POST"])
def actualizar_tituloProfesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
            
        mensaje = c_tituloProfesional.actualizar_tituloProfesional(id, nombre, descripcion, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Titulo Profesional Actualizado con Exito", "success")
            url = "/titulo_profesional"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_tituloProfesional/" + id
        return redirect(url)



@titulo_profesional_bp.route("/actualizar_estado_tituloProfesional", methods=["POST"])
def actualizar_estado_tituloProfesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_tituloProfesional.dar_baja_tituloProfesional(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Titulo Profesional Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/titulo_profesional")

    

