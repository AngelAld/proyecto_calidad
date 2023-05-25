from flask import Blueprint, render_template, request, redirect, flash, session, url_for

inicio_bp = Blueprint("inicio", __name__, template_folder="templates")


@inicio_bp.route("/inicio")
def inicio():
    if 'rol' in session:
        if session['rol'] == "Director de escuela":
            inicio ='inicio_director.html'
        else:
            if session['rol'] == "Docente de Apoyo":
                inicio = 'inicio_docente.html'
            else:
                inicio = 'inicio_estudiante.html'   
        return render_template(inicio)
    else:
        return redirect(url_for('usuario.login'))