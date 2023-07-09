from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_em as c_informe_inicial_em

informe_inicial_em_bp = Blueprint(
    "informe_inicial_em", __name__, template_folder="templates")

@informe_inicial_em_bp.route("/empresas/informes_iniciales")
def informe_inicial_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes = c_informe_inicial_em.listar_informes_iniciales_empresa()
            if isinstance(informes, list):
                return render_template("informe_inicial_em.html", informes=informes)
            else:
                flash(str(informes), "error")
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))

@informe_inicial_em_bp.route("/asd/<int:id>")
def frm_editar_informe_inicial_em(id):
    print(c_informe_inicial_em.consultar_informe_iniciales_empresa(id))
    return redirect(url_for("inicio.inicio"))  


@informe_inicial_em_bp.route("/actualizar_estado_informe_inicial_em", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_inicial_em.dar_baja_informe_inicial(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_inicial_em.informe_inicial_em"))


@informe_inicial_em_bp.route("/empresas/editar_informe_inicial/<int:id>")
def editar_informe_inicial_em(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        informe,
    ) = c_informe_inicial_em.consultar_informe_iniciales_empresa(id)
    return render_template(
        "frm_editar_informe_inicial_em.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        informe=informe,
    )

@informe_inicial_em_bp.route("/actualizar_informe_inicial_em", methods=["POST"])
def actualizar_informe_inicial_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_em = request.form["id"]
        compromiso = request.form["compromiso"]
        labores = request.form["labores"]
        firma_em = request.form["firma_empresa"]
        firma_es = request.form["firma_estudiante"]

        print(list(compromiso))
        print(list(labores))
        mensaje = 'probando'

        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/empresas/informes_iniciales"
        else:
            flash(str(mensaje), "error")
            url = "/empresas/editar_informe_inicial/" + id_informe_inicial_em
        return redirect(url)
