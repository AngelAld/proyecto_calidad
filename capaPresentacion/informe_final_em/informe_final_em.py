from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_final_em as c_informe_final_em

informe_final_em_bp = Blueprint("informe_final_em", __name__, template_folder="templates")

@informe_final_em_bp.route("/estudiante/informe_final_em")
def informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informe_final_em = c_informe_final_em.listar_informes_final_empresa()
            if isinstance(informe_final_em, list):
                return render_template("informe_final_em.html", informe_final_em=informe_final_em)
            else:
                flash(str(informe_final_em), "error")
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))


@informe_final_em_bp.route("/agregar_informe_final_em")
def agregar_informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("mantenimiento_informe_final_em.html")
    
    
@informe_final_em_bp.route("/actualizar_estado_informe_final_em", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_final_em.dar_baja_informe_final(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Final Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_final_em.informe_final_em"))
    

@informe_final_em_bp.route("/eliminar__informe_final_em", methods=["POST"])
def eliminar_informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_informe_final_em.eliminar_informe_final_em(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Informe Final Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/estudiante/informe_final_em")
    
@informe_final_em_bp.route("/estudiante/editar_informe_final/<int:id>")
def editar_informe_final_em(id):
    (
        estudiante,
        datos_cppp
    ) = c_informe_final_em.consultar_informe_final_empresa(id)

    
    return render_template(
        "frm_editar_informe_final_em.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp
    )

@informe_final_em_bp.route("/actualizar_informe_final_em", methods=["POST"])
def actualizar_informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_es = request.form['id_informe_inicial_es']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        firma_es = request.form['firma_estudiante']
        firma_jefe = request.form['firma_jefe']
        
        objetivos = request.form.getlist('objetivo[]')
        
        # plan trabajo
        n_semanas = request.form.getlist('n_semana[]')
        fs_inicio = request.form.getlist('fecha_in[]')
        fs_fin = request.form.getlist('fecha_fin[]')
        actividades = request.form.getlist('actividad[]')
        horas = request.form.getlist('horas[]')

        print(list(objetivos))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(list(horas))
        
        mensaje = 'Probando'


        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/estudiante/informes_iniciales"
        else:
            flash(str(mensaje), "error")
            url = "/estudiante/editar_informe_inicial/" + id_informe_inicial_es
        return redirect(url)



