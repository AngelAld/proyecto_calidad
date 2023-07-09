from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_facultad as c_facultad


facultad_bp = Blueprint("facultad", __name__, template_folder="templates")

@facultad_bp.route("/facultad")
def facultades():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            facultades = c_facultad.listar_facultades()
            if isinstance(facultades, list):
                return render_template("facultades.html", facultades=facultades)
            else:
                print(str(facultades))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener facultades: {e}")
            return redirect(url_for("inicio.inicio"))

@facultad_bp.route("/agregar_facultad")
def formulario_agregar_facultad():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_facultad.html")


@facultad_bp.route("/guardar_facultad", methods=["POST"])
def guardar_facultad():
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
        mensaje = c_facultad.agregar_facultad(nombre, descripcion, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Facultad Registrado con Exito", "success")
            url = "/facultades"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_facultad"

        return redirect(url)


@facultad_bp.route("/facultades")
def semestres():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultades = c_facultad.listar_facultades()
        return render_template("facultades.html", facultades=facultades)


@facultad_bp.route("/eliminar_facultad", methods=["POST"])
def eliminar_facultad():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_facultad.eliminar_facultad(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Facultad Eliminada con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/facultades")


@facultad_bp.route("/formulario_editar_facultad/<int:id>")
def editar_facultad(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultades = c_facultad.buscar_facultad(id)
        return render_template("frm_editar_facultad.html", facultades=facultades)
   
    
@facultad_bp.route("/actualizar_facultad", methods=["POST"])
def actualizar_facultad():
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
    
        mensaje = c_facultad.actualizar_facultad(id,nombre, descripcion, estado)
        if mensaje == "Operación realizada con éxito":
            flash(f"Facultad Actualizada con Exito", "success")
            url = "/facultad"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_facultad/" + id
        return redirect(url)
    

@facultad_bp.route("/actualizar_estado_facultad", methods=["POST"])
def actualizar_estado_facultad():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_facultad.dar_baja_facultad(id, estado)
        if mensaje == "Operación realizada con éxito":
            flash(f"Facultad Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/facultades")


@facultad_bp.route("/reporte_facultad")
def formulario_reporte_facultad():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        datos,nombres_facultad = c_facultad.grafico_facultad()   
        return render_template("reporte_facultad.html", datos=datos, nombres_facultad=nombres_facultad)