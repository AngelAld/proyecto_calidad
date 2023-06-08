from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es


informe_inicial_es_bp = Blueprint("informe_inicial_es", __name__, template_folder="templates")

@informe_inicial_es_bp.route("/informe_inicia_es")
def informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_inicial_es = c_informe_inicial_es.getAll()
        return render_template("informes_inicial_es.html", informe_inicial_es=informe_inicial_es)

