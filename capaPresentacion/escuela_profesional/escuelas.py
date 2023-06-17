from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_escuela as c_escuela


escuela_bp = Blueprint("escuela", __name__, template_folder="templates")


@escuela_bp.route("/escuela")
def escuelas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        escuela = c_escuela.getAll()
        return render_template("escuelas.html", escuela=escuela)


