from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es

informe_inicial_es_bp = Blueprint("informe_inicial_es", __name__, template_folder="templates")

@informe_inicial_es_bp.route("/informe_inicia_es")
def informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        informe_inicial_es = c_informe_inicial_es.listar_informe_inicial_es()
        return render_template("informe_inicial_es.html", informe_inicial_es=informe_inicial_es)
    
@informe_inicial_es_bp.route("/agregar_informe_inicial_es")
def agregar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:  
       nomEstudiante = c_informe_inicial_es.obtener_nombre_estudiante()
       codigoEstudiante = c_informe_inicial_es.obtener_codigo_estudiante()
       semestreEstudiante = c_informe_inicial_es.obtener_semestre_estudiante()
       razonSocialCpp = c_informe_inicial_es.obtener_razon_social_cpp()
       NomResponsableCpp = c_informe_inicial_es.obtener_nombre_responsable_practica()
       CarResponsableCpp = c_informe_inicial_es.obtener_cargo_responsable_practica()

       return render_template("mantenimiento_informe_inicial_es.html",nomEstudiante=nomEstudiante,codigoEstudiante=codigoEstudiante,semestreEstudiante=semestreEstudiante,razonSocialCpp=razonSocialCpp,NomResponsableCpp=NomResponsableCpp,CarResponsableCpp=CarResponsableCpp) 
