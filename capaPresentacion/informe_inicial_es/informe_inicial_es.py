from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es

informe_inicial_es_bp = Blueprint(
    "informe_inicial_es", __name__, template_folder="templates"
)


@informe_inicial_es_bp.route("/estudiantes/informes_iniciales")
def informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes = c_informe_inicial_es.listar_informes_iniciales_estudiante()
            if isinstance(informes, list):
                return render_template("informe_inicial_es.html", informes=informes)
            else:
                flash(str(informes), "error")
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))


@informe_inicial_es_bp.route("/asd/<int:id>")
def frm_editar_informe_inicial_es(id):
    print(c_informe_inicial_es.consultar_informe_iniciales_estudiante(id))
    return redirect(url_for("inicio.inicio"))


@informe_inicial_es_bp.route("/actualizar_estado_informe_inicial_es", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_inicial_es.dar_baja_informe_inicial(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_inicial_es.informe_inicial_es"))


@informe_inicial_es_bp.route("/estudiante/editar_informe_inicial/<int:id>")
def editar_informe_inicial_es(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        objetivos,
        planes_trabajo,
        informe,
    ) = c_informe_inicial_es.consultar_informe_iniciales_estudiante(id)

    
    return render_template(
        "frm_editar_informe_inicial_es.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        objetivos=objetivos,
        planes_trabajo=planes_trabajo,
        informe = informe,
    )


@informe_inicial_es_bp.route("/actualizar_informe_inicial_es", methods=["POST"])
def actualizar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_es = request.form["id"]
        estado = request.form.get("estado")
        id_detalle_practica = request.form["id_detalle_practica"]

        mensaje = c_informe_inicial_es.actualizar_informe_inicial_es(
            id_informe_inicial_es, estado, id_detalle_practica
        )

        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_informe_inicial/" + id_informe_inicial_es
        return redirect(url)
