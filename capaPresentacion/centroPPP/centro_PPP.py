from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_cppp as c_cppp

cPPP_bp = Blueprint("centroPPP", __name__, template_folder="templates")

@cPPP_bp.route("/centro_PPP")
def centro_PPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        centro_PPP = c_cppp.listar_cppp()
        return render_template("centroPPP.html", centro_PPP = centro_PPP)
    
@cPPP_bp.route("/agregar_centroPPP")
def formulario_agregar_CentroPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_CentroPPP.html")
    
@cPPP_bp.route("/guardar_centroPPP", methods=["POST"])
def guardar_centroPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        ruc = request.form["ruc"]
        razon_social = request.form["razon_social"]
        alias = request.form["alias"]
        rubro = request.form["rubro"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        id_ubicacion = request.form["id_ubicacion"]
        mensaje = c_cppp.agregar_centroPPP(ruc, razon_social, alias, rubro, telefono, correo, id_ubicacion)
        if mensaje == "Operación realizada con éxito":
            flash(f"Centro de Practicas Pre Profesionales Registrado con Exito", "success")
            url = "/centro_PPP"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_centroPPP"

        return redirect(url)
    
@cPPP_bp.route("/eliminar_CentroPPP", methods=["POST"])
def eliminar_CentroPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        centro_PPP = c_cppp.eliminar_centroPPP(request.form["id"])
        if centro_PPP == "Operación realizada con éxito":
            flash(f"Centro de Practica Eliminado con Exito", "success")
        else:
            flash(str(centro_PPP), "error")
        return redirect("/centro_PPP")
    
@cPPP_bp.route("/formulario_editar_centroPPP/<int:id>")
def editar_centroPPP(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        centro_PPP = c_cppp.obtener_cpppID(id)
        return render_template("frm_editar_centroPPP.html", centro_PPP=centro_PPP)
        
@cPPP_bp.route("/modificar_centroPPP", methods=["POST"])
def modificar_centroPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        #id = request.form["id"]
        ruc = request.form["ruc"]
        razon_social = request.form["razon_social"]
        alias = request.form["alias"]
        rubro = request.form["rubro"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        # frm_estado = request.form.get("estado")
        # if frm_estado == "on":
        #     estado = "A"
        # else:
        #     estado = "I"
        #null = request.form["null"]
        id_ubicacion = request.form["id_ubicacion"]
        mensaje = c_cppp.agregar_centroPPP(ruc, razon_social,alias, rubro, telefono, correo, id_ubicacion)

        if mensaje == "Operación realizada con éxito":
            flash(f"Centro de Practicas Actualizado con Exito", "success")
            url = "/centro_PPP"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_centroPPP/" + id
        return redirect(url)
            
@cPPP_bp.route("/actualizar_estado_CPPP", methods=["POST"])
def actualizar_estado_CPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_cppp.dar_baja_CPPP(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"CPPP Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/centro_PPP")
    

