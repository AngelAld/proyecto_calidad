from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_jefe_inmediato as c_jefe_inmediato


jefe_inmediato_bp = Blueprint("jefe_inmediato", __name__, template_folder="templates")

@jefe_inmediato_bp.route("/jefe_inmediato")
def jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        jefe_inmediato = c_jefe_inmediato.listar_jefe_inmediato()
        return render_template("jefe_inmediato.html", jefe_inmediato=jefe_inmediato)


@jefe_inmediato_bp.route("/agregar_jefe_inmediato")
def formulario_agregar_jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_jefe_inmediato.html")


@jefe_inmediato_bp.route("/guardar_jefe_inmediato", methods=["POST"])
def guardar_jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        cargo = request.form["cargo"]
        id_centro_practica = request.form["centro_practica"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        mensaje = c_jefe_inmediato.agregar_jefe_inmediato(nombre,correo, telefono, cargo, id_centro_practica, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Jefe inmediato Registrado con Exito", "success")
            url = "/jefe_inmediato"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_jefe_inmediato"

        return redirect(url)




@jefe_inmediato_bp.route("/eliminar_jefe_inmediato", methods=["POST"])
def eliminar_jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_jefe_inmediato.eliminar_jefe_inmediato(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Jefe Inmediato Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/jefe_inmediato")


@jefe_inmediato_bp.route("/formulario_editar_jefe_inmediato/<int:id>")
def editar_jefe_inmediato(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        jefe_inmediato = c_jefe_inmediato.buscar_jefe_inmediatoID(id)
        return render_template("frm_editar_jefe_inmediato.html", jefe_inmediato=jefe_inmediato)


@jefe_inmediato_bp.route("/actualizar_jefe_inmediato", methods=["POST"])
def actualizar_jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        cargo = request.form["cargo"]
        id_centro_practica = request.form["centro_practica"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        mensaje = c_jefe_inmediato.actualizar_jefe_inmediato(id, nombre, correo, telefono, cargo,id_centro_practica, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Jefe inmediato actualizado con Exito", "success")
            url = "/jefe_inmediato"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_jefe_inmediato/" + id
        return redirect(url)


@jefe_inmediato_bp.route("/actualizar_estado_jefe_inmediato", methods=["POST"])
def actualizar_estado_jefe_inmediato():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_jefe_inmediato.dar_baja_jefe_inmediato(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Jefe Inmediato actualizado con éxito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/jefe_inmediato")
