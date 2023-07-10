from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_ficha_desempeno as c_ficha_desempeno
from werkzeug.utils import secure_filename
import os
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/files/iie'

ficha_desempeno_bp = Blueprint("ficha_desempeno", __name__, template_folder="templates")

@ficha_desempeno_bp.route("/ficha_desempeno")
def ficha_desempeno():
    rol = session.get("rol")
    if not rol or (rol != "Docente de Apoyo" and rol != "Estudiante"):
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            ficha_desempenos = c_ficha_desempeno.listar_fichas_desempeno()
            if isinstance(ficha_desempenos,list):
                return render_template("ficha_desempeno.html", ficha_desempenos=ficha_desempenos)
            else:
                print(str(ficha_desempenos))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener fichas de desempeño: {e}")
            return redirect(url_for("inicio.inicio"))            

@ficha_desempeno_bp.route("/agregar_ficha_desempeno")
def agregar_ficha_desempeno():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template("mantenimiento_ficha_desempeno.html")
    
@ficha_desempeno_bp.route("/actualizar_estado_ficha_desempeno", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_ficha = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_ficha_desempeno.dar_baja_ficha_desempeno(id_ficha, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Ficha de Desempeño Actualizada con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("ficha_desempeno.ficha_desempeno"))

@ficha_desempeno_bp.route("/estudiante/editar_ficha_desempeno/<int:id>")
def editar_ficha_desempeno(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        resultados_aprendizaje,
        ficha_desempeno,
        conclusiones,
    ) = c_ficha_desempeno.consultar_ficha_desempeno(id)

    return render_template(
        "frm_editar_ficha_desempeno.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        resultados_aprendizaje=resultados_aprendizaje,
        ficha_desempeno=ficha_desempeno,
        conclusiones=conclusiones,
    )


@ficha_desempeno_bp.route("/actualizar_ficha_desempeno", methods=["POST"])
def actualizar_ficha_desempeno():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            id_ficha_desempeno = request.form['id_ficha_desempeno']
            area_desempeno = request.form['area_desempeno']
            conclusiones = request.form['conclusiones']
            responsabilidad = request.form['responsabilidad']
            proactividad = request.form['proactividad']
            comunicacion= request.form['comunicacion']
            trabajoequipo=request.form['trabajoequipo']
            compromiso=request.form['compromiso']
            organizacion=request.form['organizacion']
            puntualidad=request.form['puntualidad']

            firma_em = ""
            if 'firma' in request.files:
                f = request.files['firma']
                if f.filename != '':
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(UPLOAD_FOLDER, filename))
                    firma_em = os.path.join(UPLOAD_FOLDER, filename)

            resultados_aprendizaje = []
            resultados = request.form.getlist('resultado[]')
            escala = request.form.getlist('escala[]')
            for i in range(len(resultados)):
                resultados_aprendizaje.append({
                    "escala": escala[i],
                    "descripcion": resultados[i]
                })

            mensaje = c_ficha_desempeno.actualizar_ficha_desempeno(id_ficha_desempeno,area_desempeno,conclusiones,responsabilidad,proactividad,comunicacion,trabajoequipo,compromiso,organizacion,puntualidad, firma_em, resultados_aprendizaje)

            if mensaje == "Operación realizada con éxito":
                flash("Ficha de Evaluación de Desempeño actualizada con éxito", "success")
                url = "/ficha_desempeno"  # Reemplaza con la URL de redireccionamiento exitoso
            else:
                flash(str(mensaje), "error")
                url = "/estudiante/editar_ficha_desempeno/" + id_ficha_desempeno  # Reemplaza con la URL de redireccionamiento de error

            return redirect(url)

        except Exception as e:
            flash("Error al actualizar la ficha de desempeño: " + str(e), "error")
            return redirect(url_for("inicio.inicio"))


