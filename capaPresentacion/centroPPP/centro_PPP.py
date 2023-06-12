from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_cppp as c_cppp

cPPP_bp = Blueprint("centroPPP", __name__, template_folder="templates")

@cPPP_bp.route("/agregar_centroPPP")
def formulario_agregar_CentroPPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("frm_agregar_CentroPPP.html")
    
@cPPP_bp.route("/centro_PPP")
def centro_PPP():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        centro_PPP = c_cppp.getAll()
        return render_template("centroPPP.html", centro_PPP=centro_PPP)

