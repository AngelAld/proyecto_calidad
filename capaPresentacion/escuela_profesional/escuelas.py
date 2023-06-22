from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_escuela as c_escuela
from capaNegocio import controlador_facultad as c_facultad


escuela_bp = Blueprint("escuela", __name__, template_folder="templates")


@escuela_bp.route("/escuela")
def escuelas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_escuela.listar_escuela()
        return render_template("escuelas.html", escuelas=escuelas)
    
@escuela_bp.route("/escuela")
def cargar_facultad():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_facultad.cargar_facultades()
        return render_template("escuelas.html", escuelas=escuelas)
    
    
@escuela_bp.route("/agregar_escuela")
def formulario_agregar_escuela():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_escuela.html")


@escuela_bp.route("/guardar_escuela", methods=["POST"])
def guardar_escuela():
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
        id_facultad = request.form["id_facultad"]
        
        mensaje = c_escuela.agregar_escuela(nombre, descripcion, estado, id_facultad)

        if mensaje == "Operación realizada con éxito":
            flash(f"Escuela Registrado con Exito", "success")
            url = "/escuelas"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_escuelas"

        return redirect(url)


@escuela_bp.route("/escuelas")
def semestres():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_escuela.listar_escuela()
        return render_template("escuelas.html", escuelas=escuelas)


@escuela_bp.route("/eliminar_escuela", methods=["POST"])
def eliminar_escuela():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_escuela.eliminar_escuela(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Escuela Eliminada con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/escuelas")


@escuela_bp.route("/formulario_editar_escuela/<int:id>")
def editar_escuelas(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_escuela.buscar_escuela(id)
        return render_template("frm_editar_escuela.html", escuelas=escuelas)


@escuela_bp.route("/actualizar_escuela", methods=["POST"])
def actualizar_escuela():
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
        id_facultad = request.form["id_facultad"]

        mensaje = c_escuela.actualizar_escuela(id, nombre, descripcion, estado, id_facultad)
        if mensaje == "Operación realizada con éxito":
            flash(f"Escuela Actualizada con Exito", "success")
            url = "/escuelas"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_escuela/" + id
        return redirect(url)
    

@escuela_bp.route("/actualizar_estado_escuela", methods=["POST"])
def actualizar_estado_escuela():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_escuela.dar_baja_escuela(id, estado)
        if mensaje == "Operación realizada con éxito":
            flash(f"Escuela Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/escuelas")
