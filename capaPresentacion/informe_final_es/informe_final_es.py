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
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        total_horas = request.form["totalHoras"]
        # Subir archivos de firma
        firma_es = ""
        firma_jefe = ""

        if 'firma_estudiante' in request.files:
            f = request.files['firma_estudiante']
            if f.filename != '':
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_es = os.path.join(UPLOAD_FOLDER, filename)

        if 'firma_jefe' in request.files:
            f = request.files['firma_jefe']
            if f.filename != '':
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_jefe = os.path.join(UPLOAD_FOLDER, filename)

        objetivos = request.form.getlist('objetivo[]')

        # Agregar datos de planes de trabajo a una lista
        plan_trabajo = []
        n_semanas = request.form.getlist('n_semana[]')
        fs_inicio = request.form.getlist('fecha_in[]')
        fs_fin = request.form.getlist('fecha_fin[]')
        actividades = request.form.getlist('actividad[]')
        horas = request.form.getlist('horas[]')

        for i in range(len(n_semanas)):
            plan_trabajo.append({
                "n_semana": i + 1,
                "fecha_inicio": fs_inicio[i],
                "fecha_fin": fs_fin[i],
                "actividad": actividades[i],
                "horas": horas[i]
            })

        mensaje = c_informe_final_es.actualizar_informe_final(fecha_fin=fecha_fin, fecha_inicio=fecha_inicio,
                                                              id_informe_final_es=id_informe_final_es,
                                                              firma_es=firma_es, firma_jefe=firma_jefe,
                                                              descripciones=objetivos, plan_trabajo=plan_trabajo,
                                                              totalHoras=total_horas)
        print(mensaje)
        if mensaje == "Operacion realizada con éxito":
            flash("Informe Final Actualizado con Éxito", "success")
            url = "/estudiante/informes_finales"
        else:
            print('entramos aqui')
            flash(mensaje, "error")
            url = "/estudiante/editar_informe_final/" + id_informe_final_es
        return redirect(url)


    


