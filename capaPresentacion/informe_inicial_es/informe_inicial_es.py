from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es

informe_inicial_es_bp = Blueprint("informe_inicial_es", __name__, template_folder="templates")

@informe_inicial_es_bp.route("/informe_inicia_es")
def informe_inicial_es():
    rol = session.get("rol")
    if not rol or (rol !="Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        informe_inicial_es = c_informe_inicial_es.listar_informe_inicial_es()
        return render_template("informe_inicial_es.html", informe_inicial_es=informe_inicial_es)
    
@informe_inicial_es_bp.route("/agregar_informe_inicial_es")
def agregar_informe_inicial_es():
    rol = session.get("rol")
    if not rol or (rol !="Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:  
        datos_estudiantes = c_informe_inicial_es.listar_datos_estudiante()
        #id_estudiante = session.get("id_estudiante") 
        #datos_estudiantes = c_informe_inicial_es.listar_datos_estudiante(id_estudiante)
        datos_centro_especial = c_informe_inicial_es.listar_datos_centro_practica()
        return render_template("mantenimiento_informe_inicial_es.html",datos_estudiantes=datos_estudiantes, datos_centro_especial=datos_centro_especial) 



@informe_inicial_es_bp.route("/actualizar_estado_informe_inicial", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        id_detalle_practica = request.form["id_detalle_practica"]

        mensaje = c_informe_inicial_es.actualizar_informe_inicial_es(id_informe, estado, id_detalle_practica)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_informe_inicial/" + id_informe
        return redirect(url)

@informe_inicial_es_bp.route("/actualizar_informe_inicial_es", methods=["POST"])
def editar_informe_inicial_es():
    rol = session.get("rol")
    if not rol or (rol !="Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_es = request.form["id"]
        estado = request.form.get("estado")
        id_detalle_practica = request.form["id_detalle_practica"]

        mensaje = c_informe_inicial_es.actualizar_informe_inicial_es(id_informe_inicial_es, estado, id_detalle_practica)

        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_informe_inicial/" + id_informe_inicial_es
        return redirect(url)


@informe_inicial_es_bp.route("/eliminar_informe_inicial_es", methods=["POST"])
def eliminar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        mensaje = c_informe_inicial_es.eliminar_informe_inicial_es(id)

        if mensaje == "Operación realizada con éxito":
            flash(f"Informe Inicial Eliminado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/informe_inicial_es"

        return redirect(url)   