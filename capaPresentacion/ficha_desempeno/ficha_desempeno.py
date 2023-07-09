from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_ficha_desempeno as c_ficha_desempeno

ficha_desempeno_bp = Blueprint("ficha_desempeno", __name__, template_folder="templates")

@ficha_desempeno_bp.route("/ficha_desempeno")
def ficha_desempeno():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
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
    ) = c_ficha_desempeno.consultar_ficha_desempeno(id)

    return render_template(
        "frm_editar_ficha_desempeno.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        resultados_aprendizaje=resultados_aprendizaje,
        ficha_desempeno=ficha_desempeno,
    )

@ficha_desempeno_bp.route("/actualizar_ficha_desempeno", methods=["POST"])
def actualizar_ficha_desempeno():
    return 'a'