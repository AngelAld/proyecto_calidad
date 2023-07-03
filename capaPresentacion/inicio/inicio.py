from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import capaNegocio.controlador_semestres as c_semestres
inicio_bp = Blueprint("inicio", __name__, template_folder="templates")


@inicio_bp.route("/inicio")
def inicio():
    if 'rol' in session:
        if session['rol'] == "Director de escuela":
            datos = c_semestres.grafico_semestres()
            inicio ='inicio_director.html'
        else:
            if session['rol'] == "Docente de Apoyo":
                datos = c_semestres.grafico_semestres()
                inicio = 'inicio_docente.html'
            else:
                datos = c_semestres.grafico_semestres()
                inicio = 'inicio_estudiante.html'   
        return render_template(inicio, datos=datos)
    else:
        return redirect(url_for('usuario.login'))
    

    