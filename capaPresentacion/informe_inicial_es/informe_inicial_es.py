from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es

informe_inicial_es_bp = Blueprint("informe_inicial_es", __name__, template_folder="templates")

@informe_inicial_es_bp.route("/estudiante/informeinicial")
def informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes = c_informe_inicial_es.listar_informes_iniciales_estudiante()
            if isinstance(informes, list):
                return render_template("informe_inicial_es.html", informes=informes)
            else:
                print(str(informes))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))












@informe_inicial_es_bp.route("/agregar_informe_inicial_es")
def agregar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:  
        estudiantes = c_informe_inicial_es.obtener_nombre_estudiante()
        codigoEstudiante = c_informe_inicial_es.obtener_codigo_estudiante()
        semestreEstudiante = c_informe_inicial_es.obtener_semestre_estudiante()
        razonSocialCpp = c_informe_inicial_es.obtener_razon_social_cpp()
        NomResponsableCpp = c_informe_inicial_es.obtener_nombre_responsable_practica()
        CarResponsableCpp = c_informe_inicial_es.obtener_cargo_responsable_practica()

        return render_template("mantenimiento_informe_inicial_es.html",estudiantes=estudiantes,codigoEstudiante=codigoEstudiante,semestreEstudiante=semestreEstudiante,razonSocialCpp=razonSocialCpp,NomResponsableCpp=NomResponsableCpp,CarResponsableCpp=CarResponsableCpp) 
    
@informe_inicial_es_bp.route("/actualizar_estado_informe_inicial", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        id_detalle_practica = request.form["id_detalle_practica"]

        mensaje = c_informe_inicial_es.actualizar_informe_inicial_es(id_informe, estado, id_detalle_practica)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_informe_inicial/" + id_informe
        return redirect(url)

@informe_inicial_es_bp.route("/actualizar_informe_inicial_es", methods=["POST"])
def editar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_es = request.form["id"]
        estado = request.form.get("estado")
        id_detalle_practica = request.form["id_detalle_practica"]

        mensaje = c_informe_inicial_es.actualizar_informe_inicial_es(id_informe_inicial_es, estado, id_detalle_practica)

        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_informe_inicial/" + id_informe_inicial_es
        return redirect(url)


@informe_inicial_es_bp.route("/eliminar_informe_inicial_es", methods=["POST"])
def eliminar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        mensaje = c_informe_inicial_es.eliminar_informe_inicial_es(id)

        if mensaje == "Operación realizada con éxito":
            flash(f"Informe Inicial Eliminado con Éxito", "success")
            url = "/informe_inicial_es"
        else:
            flash(str(mensaje), "error")
            url = "/informe_inicial_es"

        return redirect(url)   