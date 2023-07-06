from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from capaNegocio import controlador_Estudiante as c_estudiante
import pandas as pd
from werkzeug.utils import secure_filename

estudiante_bp = Blueprint("estudiante", __name__, template_folder="templates")


@estudiante_bp.route("/agregar_estudiante")
def formulario_agregar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        planestudio = c_estudiante.obtener_planestudio()
        semesteacademico = c_estudiante.obtener_semesteacademico()
        return render_template("frm_agregar_estudiante.html",planestudio=planestudio,semesteacademico=semesteacademico)

@estudiante_bp.route("/importar_estudiantes")
def importar_estudiantes():
    return render_template('subir_excel.html')



@estudiante_bp.route("/registros_cargados", methods=['post'])
def subir_excel():
    try:
        archivo = request.files['file']
        df = pd.read_excel(archivo)
        registros = []
        for index, row in df.iterrows():    
            registro = [row['Codigo Universitario'], 
                        row['Nombres'],
                        row['Escuela Profesional'], 
                        row['DNI'], 
                        row['Correo1'], 
                        row['Correo2'],
                        row['Telefono1'],
                        row['Telefono2']]
            registros.append(registro)
        return render_template('subir_excel.html', registros=registros, archivo = archivo)
    except KeyError:
        flash('El archivo no se ha subido correctamente', 'error')
        return redirect('/importar_estudiantes')
    except ValueError:
        flash('El archivo no tiene un formato válido', 'error')
        return redirect('/importar_estudiantes')
    except Exception as e:
        flash('Ha ocurrido un error inesperado: {}'.format(str(e)), 'error')
        return redirect('/importar_estudiantes')




@estudiante_bp.route("/guardar_estudiante", methods=["POST"])
def guardar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        cod_universitario = request.form["cod_universitario"]
        dni = request.form["dni"]
        nombre = request.form["nombre"]
        correo_usat = request.form["correo_usat"]
        correo_personal = request.form["correo_personal"]
        telefono = request.form["telefono"]
        telefono2 = request.form["telefono2"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_semestre_academico_ingreso = request.form["semesteacademico"]
        id_plan_estudio = request.form['planestudio']

        mensaje = c_estudiante.insert(cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_semestre_academico_ingreso,id_plan_estudio)

        if mensaje == "Operación realizada con éxito":
            flash(f"Estudiante Registrado con Exito", "success")
            url = "/estudiante"
        else:
            flash(str(mensaje), "error")
            url = "/agregar_estudiante"

        return redirect(url)


@estudiante_bp.route("/estudiante")
def estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiante = c_estudiante.getAll()
        return render_template("estudiante.html", estudiante=estudiante)


@estudiante_bp.route("/eliminar_estudiante", methods=["POST"])
def eliminar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_estudiante.delete(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Estudiante Eliminado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/estudiante")


@estudiante_bp.route("/formulario_editar_estudiante/<int:id>")
def editar_estudiante(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiante = c_estudiante.getById(id)
        planestudio= c_estudiante.obtener_planestudio()
        semesteacademico= c_estudiante.obtener_semesteacademico()
        return render_template("frm_editar_estudiante.html", estudiante=estudiante,planestudio=planestudio,semesteacademico=semesteacademico)

@estudiante_bp.route("/actualizar_estudiante", methods=["POST"])
def actualizar_estudiante():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        cod_universitario = request.form["cod_universitario"]
        dni = request.form["dni"]
        nombre = request.form["nombre"]
        correo_usat = request.form["correo_usat"]
        correo_personal = request.form["correo_personal"]
        telefono = request.form["telefono"]
        telefono2 = request.form["telefono2"]
        frm_estado = request.form.get("estado")
        if frm_estado == "on":
            estado = "A"
        else:
            estado = "I"
        id_semestre_academico_ingreso = request.form["semesteacademico"]
        id_plan_estudio = request.form['planestudio']
        
        mensaje = c_estudiante.update(id, cod_universitario,dni,nombre,correo_usat,correo_personal,telefono, telefono2,  estado,id_semestre_academico_ingreso,id_plan_estudio)

        if mensaje == "Operación realizada con éxito":
            flash(f"Estudiante Actualizado con Exito", "success")
            url = "/estudiante"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_estudiante/" + id
        return redirect(url)


@estudiante_bp.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_estudiante.update_estado(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Estado Actualizado con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/estudiante")
    
# solo cmb-----------------------------------------
@estudiante_bp.route("/cmb_planestudio")
def cmb_planestudio():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        planestudio = c_estudiante.obtener_planestudio()
        return render_template("estudiante.html", planestudio=planestudio)
    
@estudiante_bp.route("/cmb_semesteacademico")
def cmb_semesteacademico():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        semesteacademico = c_estudiante.obtener_semesteacademico()
        return render_template("estudiante.html", semesteacademico=semesteacademico)