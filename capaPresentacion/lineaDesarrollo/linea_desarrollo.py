from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_lineadesarrollo as c_lineaDesarrollo


linea_desarrollo_bp = Blueprint("lineaDesarrollo", __name__, template_folder="templates")

@linea_desarrollo_bp.route("/linea_desarrollo")
def linea_desarrollo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        linea_desarrollo = c_lineaDesarrollo.listar_lineaDesarrollo()
        return render_template("lineaDesarrollo.html", linea_desarrollo=linea_desarrollo)


@linea_desarrollo_bp.route("/agregar_lineaDesarrollo")
def formulario_agregar_lineaDesarrollo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_lineaDesarrollo.obtener_escuelas()
        return render_template("frm_agregar_lineaDesarrollo.html", escuelas=escuelas)


@linea_desarrollo_bp.route("/guardar_lineaDesarrollo", methods=["POST"])
def guardar_lineaDesarrollo():
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
        id_escuela_profesional = request.form["escuelas"]
        
        mensaje = c_lineaDesarrollo.agregar_lineaDesarrollo(nombre, descripcion, estado,id_escuela_profesional)

        if mensaje == "Operación realizada con éxito":
            flash(f"Línea de Desarrollo Registrada con Exito", "success")
            url = "/linea_desarrollo"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_lineaDesarrollo"
            
        return redirect(url)


@linea_desarrollo_bp.route("/eliminar_lineaDesarrollo", methods=["POST"])
def eliminar_lineaDesarrollo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_lineaDesarrollo.eliminar_lineaDesarrollo(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Línea de Desarrollo Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect("/linea_desarrollo")


@linea_desarrollo_bp.route("/formulario_editar_lineaDesarrollo/<int:id>")
def editar_lineaDesarrollo(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        lineaDesarrollo = c_lineaDesarrollo.buscar_lineaDesarrolloID(id)
        escuelas = c_lineaDesarrollo.obtener_escuelas()
        return render_template("frm_editar_lineaDesarrollo.html", lineaDesarrollo=lineaDesarrollo, escuelas=escuelas)


@linea_desarrollo_bp.route("/actualizar_lineaDesarrollo", methods=["POST"])
def actualizar_lineaDesarrollo():
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
            
        id_escuela_profesional = request.form["escuelas"]
        
        mensaje = c_lineaDesarrollo.actualizar_lineaDesarrollo(id, nombre, descripcion, estado,id_escuela_profesional)

        if mensaje == "Operación realizada con éxito":
            flash(f"Línea de Desarrollo Actualizado con Exito", "success")
            url = "/linea_desarrollo"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_lineaDesarrollo/" + id
        return redirect(url)




@linea_desarrollo_bp.route("/actualizar_estado_lineaDesarrollo", methods=["POST"])
def actualizar_estado_lineaDesarrollo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_lineaDesarrollo.dar_baja_lineaDesarrollo(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Línea de Desarrollo Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/linea_desarrollo")

    

#********************************************* Lo uso para listar en combo a linea de desarrollo (NO BORRAR ESTA FUNCION) *

@linea_desarrollo_bp.route("/cmb_escuelas")
def cmb_escuelas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_lineaDesarrollo.obtener_escuelas()
        return render_template("lineaDesarrollo.html", escuelas=escuelas)


@linea_desarrollo_bp.route("/cmb_facultades")
def cmb_facultades():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultades = c_lineaDesarrollo.obtener_facultades()
        return render_template("lineaDesarrollo.html", facultades=facultades)
#***************************************************************