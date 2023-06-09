from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_planestudio as c_planEstudio 


plan_estudio_bp = Blueprint("planEstudio", __name__, template_folder="templates")

@plan_estudio_bp.route("/plan_estudio")
def plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            plan_estudio = c_planEstudio.listar_plan_estudio()
            escuelas = c_planEstudio.obtener_escuelas()
            if isinstance(plan_estudio,list): 
                return render_template("planEstudio.html", plan_estudio=plan_estudio, escuelas=escuelas)
            else:
                print(str(plan_estudio))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener plan de estudio: {e}")
            return redirect(url_for("inicio.inicio"))
    

#nuevo
@plan_estudio_bp.route("/agregar_plan_estudio")
def formulario_agregar_plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_planEstudio.obtener_escuelas()
        return render_template("frm_agregar_plan_estudio.html", escuelas=escuelas)
    
@plan_estudio_bp.route("/guardar_plan_estudio", methods=["POST"])
def guardar_plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        nombre = request.form["nombre"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_escuela_profesional = request.form["escuelas"]

        mensaje = c_planEstudio.agregar_plan_estudio(nombre, estado, id_escuela_profesional)

        if mensaje == "Operación realizada con éxito":
            flash(f"Plan Estudio Registrado con Exito", "success")
            url = "/plan_estudio"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_plan_estudio"

        return redirect(url)
    
@plan_estudio_bp.route("/eliminar_plan_estudio", methods=["POST"])
def eliminar_plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_planEstudio.eliminar_plan_estudio(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Plan Estudio Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/plan_estudio")

@plan_estudio_bp.route("/formulario_editar_plan_estudio/<int:id>")
def editar_plan_estudio(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        plan_estudio = c_planEstudio.buscar_plan_estudio_ID(id)
        escuelas = c_planEstudio.obtener_escuelas()
        return render_template("frm_editar_plan_estudio.html", plan_estudio=plan_estudio, escuelas=escuelas)
    
@plan_estudio_bp.route("/actualizar_plan_estudio", methods=["POST"])
def actualizar_plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        nombre = request.form["nombre"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_escuela_profesional = request.form["escuelas"]   

        mensaje = c_planEstudio.actualizar_plan_estudio(id, nombre, estado,id_escuela_profesional)

        if mensaje == "Operación realizada con éxito":
            flash(f"Plan Estudio Actualizado con Exito", "success")
            url = "/plan_estudio"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_plan_estudio/" + id
        return redirect(url)
    
@plan_estudio_bp.route("/actualizar_estado_plan_estudio", methods=["POST"])
def actualizar_estado_plan_estudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        print(estado)
        print("aquiiiii")
        mensaje = c_planEstudio.dar_baja_plan_estudio(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Plan Estudio Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/plan_estudio")
    
#********************************************* Lo uso para listar en combo las escuelas profesionales en plan de estudio (NO BORRAR ESTA FUNCION) *

@plan_estudio_bp.route("/cmb_escuelas")
def cmb_escuelas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuelas = c_planEstudio.obtener_escuelas()
        return render_template("planEstudio.html", escuelas=escuelas)
#***************************************************************
