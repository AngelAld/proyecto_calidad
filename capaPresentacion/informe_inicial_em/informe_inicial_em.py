from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_informe_inicial_em as c_informe_inicial_em
import os
from werkzeug.utils import secure_filename
import weasyprint
from weasyprint import HTML, CSS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/files/iiem'

informe_inicial_em_bp = Blueprint(
    "informe_inicial_em", __name__, template_folder="templates")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@informe_inicial_em_bp.route("/empresas/informes_iniciales")
def informe_inicial_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes = c_informe_inicial_em.listar_informes_iniciales_empresa()
            if isinstance(informes, list):
                return render_template("informe_inicial_em.html", informes=informes)
            else:
                flash(str(informes), "error")
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes: {e}")
            return redirect(url_for("inicio.inicio"))

@informe_inicial_em_bp.route("/asd/<int:id>")
def frm_editar_informe_inicial_em(id):
    print(c_informe_inicial_em.consultar_informe_iniciales_empresa(id))
    return redirect(url_for("inicio.inicio"))  



@informe_inicial_em_bp.route("/actualizar_estado_informe_inicial_em", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_informe_inicial_em.dar_baja_informe_inicial(id_informe, estado)

        if mensaje == "Operación realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
        else:
            flash(str(mensaje), "error")
        return redirect(url_for("informe_inicial_em.informe_inicial_em"))


@informe_inicial_em_bp.route("/empresas/editar_informe_inicial/<int:id>")
def editar_informe_inicial_em(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        informe,
    ) = c_informe_inicial_em.consultar_informe_iniciales_empresa(id)
    return render_template(
        "frm_editar_informe_inicial_em.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        informe=informe,
    )

@informe_inicial_em_bp.route("/actualizar_informe_inicial_em", methods=["POST"])
def actualizar_informe_inicial_em():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_informe_inicial_em = request.form["id_informe_inicial_em"]
        compromiso = request.form["compromiso"]
        labores = request.form["labores"]
        
        # subir archivo de firma
        firma_em = ""
        firma_es = ""
        
        if 'firma_empresa' in request.files:
            print('entro 1')
            f = request.files['firma_empresa']
            print(f)
            if f.filename != '':
                print('entro 2')
                print(f)
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_em = os.path.join(UPLOAD_FOLDER, filename)

        if 'firma_estudiante' in request.files:
            print('entro 1')
            f = request.files['firma_estudiante']
            print(f)
            if f.filename != '':
                print('entro 2')
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                firma_es = os.path.join(UPLOAD_FOLDER, filename)
        
        print(firma_em, firma_es)
        
        print(request.form)

        mensaje = c_informe_inicial_em.actualizar_informe_inicial_em(id_informe_inicial_em=id_informe_inicial_em,compromiso=compromiso,labores=labores,firma_em=firma_em, firma_es=firma_es)

        if mensaje == "Operacion realizada con éxito":
            flash("Informe Inicial Actualizado con Éxito", "success")
            url = "/empresas/informes_iniciales"
        else:
            print('entramos aqui')
            flash(str(mensaje), "error")
            url = "/empresas/editar_informe_inicial/" + id_informe_inicial_em
        return redirect(url)



@informe_inicial_em_bp.route("/empresas/informe_inicial/generar_pdf/<int:id>")
def generar_pdf_iie(id):
    (
        estudiante,
        datos_cppp,
        datos_practica,
        informe,
    ) = c_informe_inicial_em.consultar_informe_iniciales_empresa(id)

    datos_practica = list(datos_practica)
    informe = list(informe)

    informe[5] = convertir_fecha(informe[5])
    datos_practica[0] = convertir_fecha(datos_practica[0])
    datos_practica[1] = convertir_fecha(datos_practica[1])

    # Crear una nueva plantilla HTML a partir de la original
    template_html = render_template(
        "template.html",
        estudiante=estudiante,
        datos_cppp=datos_cppp,
        datos_practica=datos_practica,
        informe=informe,
    )

    # Definir la hoja de estilo CSS personalizada para establecer los márgenes
    style_css = 'body { margin: 0; }'

    # Crear un objeto HTML a partir de la plantilla
    html = HTML(string=template_html)

    # Crear un objeto CSS a partir de la hoja de estilo personalizada
    css = CSS(string=style_css)

    # Generar el PDF a partir del objeto HTML y la lista de objetos CSS
    pdf_bytes = html.write_pdf(page_size=(8.5, 11, 'in'),
    margin=(0.5, 0.5, 0.5, 0.5, 'in'),)

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
    