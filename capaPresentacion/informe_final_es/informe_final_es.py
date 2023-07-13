from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_final_es as c_informe_final_es
import os
from datetime import datetime, date
from werkzeug.utils import secure_filename

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

@informe_final_es_bp.route("/editar_informe_final_es/<int:id>")
def frm_editar_informe_final_es(id):
    return redirect(url_for("inicio.inicio"))


@informe_final_es_bp.route("/estudiante/editar_informe_final_es/<int:id>")
def editar_informe_final_es(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        objetivos,
        plan_trabajo,
        informe,
    ) = c_informe_final_es.consultar_informe_finales_estudiante(id)

    return render_template(
        "frm_editar_informe_final_es.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        objetivos=objetivos,
        plan_trabajo=plan_trabajo,
        informe=informe,
    )


@informe_final_es_bp.route("/actualizar_informe_final_es", methods=["POST"])
def actualizar_informe_final_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_final_es = request.form['id_informe_final_es']
        introduccion = request.form['introduccion']
        cantidad_trabajadores = request.form['cant_trabajadores']
        mision = request.form['mision']
        vision = request.form['vision']
        infra_fisica = request.form['infraFisica']
        infra_tecnologica = request.form['infraTecnologica']
        desc_labores_r = request.form['laboresEstudiante']
        conclusiones = request.form.getlist('conclusion[]')
        recomendaciones = request.form.getlist('recomendacion[]')
        bibliografia = request.form.getlist('bibliografia[]')

        mensaje = c_informe_final_es.actualizar_informe_final(id_informe_final_es, introduccion, cantidad_trabajadores, mision, vision, infra_fisica, infra_tecnologica, desc_labores_r, conclusiones, recomendaciones, bibliografia)

        print(mensaje)
        if mensaje == "Operación realizada con éxito":
            flash("Informe Final Actualizado con Éxito", "success")
            url = url_for("informe_final_es.informe_final_es")
        else:
            flash(mensaje, "error")
            url = url_for("informe_final_es.editar_informe_final_es", id=id_informe_final_es)

        return redirect(url)








    


