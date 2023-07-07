from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_escuela as c_escuela


escuela_bp = Blueprint("escuela", __name__, template_folder="templates")


@escuela_bp.route("/escuela")
def escuelas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:            
            escuelas = c_escuela.listar_escuela()
            if isinstance(escuelas, list):
                return render_template("escuelas.html", escuelas=escuelas)
            else:
                print(str(escuelas))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener escuelas: {e}")
            return redirect(url_for("inicio.inicio"))
    
#********************************************* Lo uso para listar en combo a linea de desarrollo (NO BORRAR ESTA FUNCION) *
@escuela_bp.route("/cmb_facultades")
def cmb_facultades():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultades = c_escuela.cargar_facultades()
        return render_template("escuelas.html", facultades=facultades)
    
#*********************************************         
    
@escuela_bp.route("/agregar_escuela")
def formulario_agregar_escuela():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultades = c_escuela.cargar_facultades()
        return render_template("frm_agregar_escuela.html", facultades= facultades)


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
        id_facultad = request.form["facultades"]
       
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
            #flash(str("Escuela no eliminada", "error"))
            flash(str(mensaje), "error")
        return redirect("/escuelas")


@escuela_bp.route("/formulario_editar_escuela/<int:id>")
def editar_escuelas(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_escuela.buscar_escuela(id)
        facultades = c_escuela.cargar_facultades()
        return render_template("frm_editar_escuela.html", escuelas=escuelas, facultades= facultades)


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
        id_facultad = request.form["facultades"]

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
