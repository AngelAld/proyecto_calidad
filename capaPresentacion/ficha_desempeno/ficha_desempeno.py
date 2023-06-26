from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_ficha_desempeno as c_ficha_desempeno

ficha_desempeno_bp = Blueprint("ficha_desempeno", __name__, template_folder="templates")

@ficha_desempeno_bp.route("/ficha_desempeno")
def ficha_desempeno():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        ficha_desempeno = c_ficha_desempeno.getAll()
        return render_template("ficha_desempeno.html", ficha_desempeno=ficha_desempeno)

@ficha_desempeno_bp.route("/agregar_ficha_desempeno")
def agregar_ficha_desempeno():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("mantenimiento_ficha_desempeno.html")
