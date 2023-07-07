from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_cppp as c_cppp

cPPP_bp = Blueprint("centroPPP", __name__, template_folder="templates")

@cPPP_bp.route("/centro_PPP")
def centro_PPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            centro_PPP = c_cppp.listar_cppp()
            if isinstance(centro_PPP,list):
                return render_template("centroPPP.html", centro_PPP = centro_PPP)
            else:
                print(str(centro_PPP))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener centro de Práctica: {e}")
            return redirect(url_for("inicio.inicio"))



@cPPP_bp.route("/agregar_centroPPP")
def formulario_agregar_CentroPPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_CentroPPP.html")
    
@cPPP_bp.route("/guardar_centroPPP", methods=["POST"])
def guardar_centroPPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        ruc = request.form["ruc"]
        razon_social = request.form["razon_social"]
        alias = request.form["alias"]
        rubro = request.form["rubro"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        mensaje = c_cppp.agregar_centroPPP(ruc, razon_social, alias, rubro, telefono, correo)
        if mensaje == "Operación realizada con éxito":
            flash(f"Centro de Practicas Pre Profesionales Registrado con Exito", "success")
            url = "/centro_PPP"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_centroPPP"

        return redirect(url)
    
@cPPP_bp.route("/eliminar_CentroPPP", methods=["POST"])
def eliminar_CentroPPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
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
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        centro_PPP = c_cppp.buscar_CentroPPPID(id)
        ubicacion = c_cppp.obtener_ubicacion_por_id(centro_PPP[7])
        return render_template('frm_editar_centroPPP.html', centroPPP= centro_PPP, ubicacion=ubicacion)
        
@cPPP_bp.route("/modificar_centroPPP", methods=["POST"])
def modificar_centroPPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        ruc = request.form["ruc"]
        razon_social = request.form["razon_social"]
        alias = request.form["alias"]
        rubro = request.form["rubro"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        
        mensaje = c_cppp.actualizar_centroPPP(id, ruc, razon_social,alias, rubro, telefono, correo)

        if mensaje == "Operación realizada con éxito":
            flash(f"Centro de Practicas Actualizado con Exito", "success")
            url = "/centro_PPP"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_centroPPP/" + id
        return redirect(url)
            
@cPPP_bp.route("/actualizar_estado_CPPP", methods=["POST"])
def actualizar_estado_CPPP():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
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
#***********************REPORTES****************************************
@cPPP_bp.route("/reporte_centroPractica")
def formulario_reporte_centroPractica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        datos,alias = c_cppp.grafico_centroPPP()   
        return render_template("reporte_centroPractica.html", datos=datos, alias=alias)    

@cPPP_bp.route("/ubicacion", methods=["POST"])
def ubicacion():
    id_centro_practicas = request.form["id"]
    id_ubicacion = request.form["id_ubicacion"]
    pais = request.form["pais"]
    ciudad = request.form["ciudad"]
    num = request.form["num"]
    via = request.form["via"]
    lon = request.form["lon"]
    lat = request.form["lat"]
    frm_estado = request.form.get("estado")
    if frm_estado == "on":
        estado = "A"
    else:
        estado = "P"
    
    if id_ubicacion == "None":
        mensaje = c_cppp.agregar_ubicacion(id_centro_practicas, num, via, lon, lat, pais, ciudad, estado)
    else:
        mensaje = c_cppp.actualizar_ubicacion(id_ubicacion, num, via, lon, lat, pais, ciudad, estado)
        
    if mensaje == "Operación realizada con éxito":
        flash(mensaje, "success")
    else:
        flash(mensaje, "error")

    return redirect("/formulario_editar_centroPPP/" + id_centro_practicas)