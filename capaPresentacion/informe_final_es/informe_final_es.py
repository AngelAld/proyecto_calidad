from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_final_es as c_informe_final_es

informe_final_es_bp = Blueprint("informe_final_es", __name__, template_folder="templates")

@informe_final_es_bp.route("/informe_final_es")
def informe_final_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_final_es = c_informe_final_es.getAll()
        return render_template("informe_final_es.html", informe_final_es=informe_final_es)
