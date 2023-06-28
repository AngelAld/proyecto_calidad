from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_final_em as c_informe_final_em

informe_final_em_bp = Blueprint("informe_final_em", __name__, template_folder="templates")

@informe_final_em_bp.route("/informe_final_em")
def informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_final_em = c_informe_final_em.getAll()
        return render_template("informe_final_em.html", informe_final_em=informe_final_em)

@informe_final_em_bp.route("/agregar_informe_final_em")
def agregar_informe_final_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("mantenimiento_informe_final_em.html")