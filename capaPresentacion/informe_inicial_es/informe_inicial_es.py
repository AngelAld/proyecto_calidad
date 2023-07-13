from flask import Blueprint, render_template, request, redirect, flash, session, url_for,  make_response
from capaNegocio import controlador_informe_inicial_es as c_informe_inicial_es
import os
from datetime import datetime, date
from werkzeug.utils import secure_filename
import weasyprint
from weasyprint import HTML, CSS



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/files/iie'

informe_inicial_es_bp = Blueprint(
    "informe_inicial_es", __name__, template_folder="templates"
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@informe_inicial_es_bp.route("/estudiante/informes_iniciales")
def informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes = c_informe_inicial_es.listar_informes_iniciales_estudiante()
            if isinstance(informes, list):
                return render_template("informe_inicial_es.html", informes=informes)
            else:
                flash(str(informes), "error")
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))


@informe_inicial_es_bp.route("/asd/<int:id>")
def frm_editar_informe_inicial_es(id):
    print(c_informe_inicial_es.consultar_informe_iniciales_estudiante(id))
    return redirect(url_for("inicio.inicio"))


@informe_inicial_es_bp.route("/actualizar_estado_informe_inicial_es", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_inicial_es.dar_baja_informe_inicial(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_inicial_es.informe_inicial_es"))


@informe_inicial_es_bp.route("/estudiante/editar_informe_inicial/<int:id>")
def editar_informe_inicial_es(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        objetivos,
        planes_trabajo,
        informe,
    ) = c_informe_inicial_es.consultar_informe_iniciales_estudiante(id)

    
    return render_template(
        "frm_editar_informe_inicial_es.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        objetivos=objetivos,
        planes_trabajo=planes_trabajo,
        informe = informe,
    )


@informe_inicial_es_bp.route("/actualizar_informe_inicial_es", methods=["POST"])
def actualizar_informe_inicial_es():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_es = request.form['id_informe_inicial_es']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        total_horas = request.form["totalHoras"]
        # Subir archivos de firma
        firma_es = ""
        firma_jefe = ""

        if 'firma_estudiante' in request.files:
            f = request.files['firma_estudiante']
            if f.filename != '':
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_es = os.path.join(UPLOAD_FOLDER, filename)

        if 'firma_jefe' in request.files:
            f = request.files['firma_jefe']
            if f.filename != '':
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_jefe = os.path.join(UPLOAD_FOLDER, filename)
        
        objetivos = request.form.getlist('objetivo[]')
        
        # Agregar datos de planes de trabajo a una lista
        plan_trabajo = []
        n_semanas = request.form.getlist('n_semana[]')
        fs_inicio = request.form.getlist('fecha_in[]')
        fs_fin = request.form.getlist('fecha_fin[]')
        actividades = request.form.getlist('actividad[]')
        horas = request.form.getlist('horas[]')

        for i in range(len(n_semanas)):
            plan_trabajo.append({
                "n_semana": i + 1,
                "fecha_inicio": fs_inicio[i],
                "fecha_fin": fs_fin[i],
                "actividad": actividades[i],
                "horas": horas[i]
            })



        mensaje = c_informe_inicial_es.actualizar_informe_inicial(fecha_fin=fecha_fin, fecha_inicio=fecha_inicio, id_informe_inicial_es=id_informe_inicial_es, firma_es=firma_es, firma_jefe=firma_jefe, descripciones=objetivos, plan_trabajo=plan_trabajo, totalHoras=total_horas)
        print(mensaje)
        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/estudiante/informes_iniciales"
        else:
            print('entramos aqui')
            flash(mensaje, "error")
            url = "/estudiante/editar_informe_inicial/" + id_informe_inicial_es
        return redirect(url)



@informe_inicial_es_bp.route("/estudiante/informe_inicial/generar_pdf/<int:id>")
def generar_pdf_iie(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        objetivos,
        planes_trabajo,
        informe,
    ) = c_informe_inicial_es.consultar_informe_iniciales_estudiante(id)

    datos_practica = list(datos_practica)
    informe = list(informe)
    planes_trabajo = list(planes_trabajo)
    for i in range(len(planes_trabajo)):
        planes_trabajo[i] = list(planes_trabajo[i])
        planes_trabajo[i][3] = convertir_fecha(planes_trabajo[i][3])
        planes_trabajo[i][4] = convertir_fecha(planes_trabajo[i][4])

    informe[2] = convertir_fecha(informe[2])
    datos_practica[1] = convertir_fecha(datos_practica[1])
    datos_practica[2] = convertir_fecha(datos_practica[2])

    # Crear una nueva plantilla HTML a partir de la original
    template_html = render_template(
        "template.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        objetivos=objetivos,
        planes_trabajo=planes_trabajo,
        informe=informe,
    )


    html = HTML(string=template_html)

    # Crear un objeto CSS a partir de la hoja de estilo personalizada

    # Generar el PDF a partir del objeto HTML y la lista de objetos CSS
    pdf_bytes = html.write_pdf()

    # Devolver el PDF generado como una respuesta HTTP
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=informe_inicial.pdf"
    return response    






def convertir_fecha(fecha):
    try:
        fecha_str = fecha.strftime('%Y-%m-%d')
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        fecha_formateada = fecha_dt.strftime('%d/%m/%Y')
        return fecha_formateada
    except:
        return('Fecha no registrada')
    