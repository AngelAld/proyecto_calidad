from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_facultad as c_facultad


facultad_bp = Blueprint("facultad", __name__, template_folder="templates")




@facultad_bp.route("/facultad")
def facultades():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        facultad = c_facultad.getAll()
        return render_template("facultades.html", facultad=facultad)


