from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_em as c_informe_inicial_em


informe_inicial_em_bp = Blueprint("informe_inicial_em", __name__, template_folder="templates")

@informe_inicial_em_bp.route("/informe_inicia_em")
def informe_inicial_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_inicial_es = c_informe_inicial_em.getAll()
        return render_template("informes_inicial_em.html", informe_inicial_em=informe_inicial_em)
