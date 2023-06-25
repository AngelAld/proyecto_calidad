from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_docentes as c_docentes

docentes_bp = Blueprint("docente", __name__, template_folder="templates")

@docentes_bp.route("/agregar_docente")
def formulario_agregar_docente():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        titulo = c_docentes.obtener_titulo()
        escuela_profesional = c_docentes.obtener_escuela_profesional()
        usuario = c_docentes.obtener_usuario()
        return render_template("frm_agregar_docente.html", titulo=titulo, escuela_profesional=escuela_profesional, usuario=usuario)


@docentes_bp.route("/guardar_docente", methods=["POST"])
def guardar_docente():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_titulo = request.form["titulo"]
        id_escuela_profesional = request.form["escuela_profesional"]
        id_usuario = request.form["usuario"]
        
        mensaje = c_docentes.agregar_docente(nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario)

        if mensaje == "Operación realizada con éxito":
            flash(f"Docente Registrado con Exito", "success")
            url = "/docentes"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_docente"

        return redirect(url)


@docentes_bp.route("/docentes")
def docentes():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        docentes = c_docentes.listar_docentes()
        return render_template("docentes.html", docentes=docentes)
    

@docentes_bp.route("/eliminar_docente", methods=["POST"])
def eliminar_docente():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_docentes.eliminar_docente(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Docente Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/docentes")
    

@docentes_bp.route("/formulario_editar_docente/<int:id>")
def editar_docente(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        docente = c_docentes.buscar_docenteID(id)
        titulo = c_docentes.obtener_titulo()
        escuela_profesional = c_docentes.obtener_escuela_profesional()
        usuario = c_docentes.obtener_usuario()
        return render_template("frm_editar_docente.html", docente=docente, titulo=titulo, escuela_profesional=escuela_profesional, usuario=usuario)
    

@docentes_bp.route("/actualizar_docente", methods=["POST"])
def actualizar_docente():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_titulo = request.form["titulo"]
        id_escuela_profesional = request.form["escuela_profesional"]
        id_usuario = request.form["usuario"]
        

        mensaje = c_docentes.actualizar_docente(id, nombre, correo, estado, id_titulo, id_escuela_profesional, id_usuario)

        if mensaje == "Operación realizada con éxito":
            flash(f"Docente Actualizado con Exito", "success")
            url = "/docentes"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_docente/" + id
        return redirect(url)

@docentes_bp.route("/actualizar_docente", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_docentes.actualizar_estado_docente(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Docente Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/docentes")


# solo cmb-----------------------------------------
@docentes_bp.route("/cmb_titulo")
def cmb_titulo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        titulo = c_docentes.obtener_titulo()
        return render_template("docentes.html", titulo=titulo)
    
@docentes_bp.route("/cmb_escuela_profesional")
def cmb_escuela_profesional():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuela_profesional = c_docentes.obtener_escuela_profesional()
        return render_template("docentes.html", escuela_profesional=escuela_profesional)
    
@docentes_bp.route("/cmb_usuario")
def cmb_usuario():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        usuario = c_docentes.obtener_usuario()
        return render_template("docentes.html", usuario=usuario)