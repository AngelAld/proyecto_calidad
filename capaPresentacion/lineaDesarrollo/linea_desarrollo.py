from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_lineadesarrollo as c_lineaDesarrollo


linea_desarrollo_bp = Blueprint("lineaDesarrollo", __name__, template_folder="templates")

@linea_desarrollo_bp.route("/linea_desarrollo")
def linea_desarrollo():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        linea_desarrollo = c_lineaDesarrollo.getAll()
        return render_template("lineaDesarrollo.html", linea_desarrollo=linea_desarrollo)

