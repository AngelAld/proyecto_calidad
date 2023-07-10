from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_final_es as c_informe_final_es

informe_final_es_bp = Blueprint("informe_final_es", __name__, template_folder="templates")

@informe_final_es_bp.route("/informe_final_es")
def informe_final_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_final_es = c_informe_final_es.listar_informes_finales_estudiante()
        return render_template("informe_final_es.html", informe_final_es=informe_final_es)
    
# @informe_final_es_bp.route("/agregar_informe_final_es")
# def agregar_informe_final_es():
#     if "rol" not in session or session["rol"] != "Docente de Apoyo":
#         return redirect(url_for("inicio.inicio"))
#     else:
#         return render_template("mantenimiento_informe_final_es.html")
    
@informe_final_es_bp.route("/actualizar_estado_informe_final_estudiante", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_final_es.dar_baja_informe_final_estudiante(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Final del Estudiante Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_final_es.informe_final_es"))

    


