from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_practica as c_practica


practica_bp = Blueprint("practica", __name__, template_folder="templates")


@practica_bp.route("/agregar_practica")
def formulario_agregar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_practica.html")


@practica_bp.route("/guardar_practica", methods=["POST"])
def guardar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_estudiante = request.form["id_estudiante"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        id_linea_desarrollo = request.form["id_linea_desarrollo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        id_semestre_academico = request.form["id_semestre_academico"]
        horas = request.form["horas"]
        id_jefe_inmediato = request.form["id_jefe_inmediato"]
        informacion_adicional = request.form["informacion_adicional"]

        mensaje = c_practica.agregar_practica(
            id_estudiante, estado, id_linea_desarrollo, fecha_inicio,
            fecha_fin, id_semestre_academico, horas, id_jefe_inmediato,
            informacion_adicional
        )

        if mensaje == "Operación realizada con éxito":
            flash("Práctica registrada con éxito", "success")
            url = "/practicas"
        else:
            flash(str(mensaje), "error")
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
def eliminar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_practica.eliminar_practica(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"practica Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/practicas")


@practica_bp.route("/formulario_editar_practica/<int:id>")
def editar_practica(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        practica = c_practica.buscar_practicaID(id)
        return render_template("frm_editar_practica.html", practica=practica)


@practica_bp.route("/actualizar_practica", methods=["POST"])
def actualizar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id_practica"]
        nombre = request.form["nombre"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"

        mensaje = c_practica.actualizar_practica(id, nombre, fecha_inicio, fecha_fin, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"practica Actualizado con Exito", "success")
            url = "/practicas"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_practica/" + id
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
            flash(f"practica Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/practicas")