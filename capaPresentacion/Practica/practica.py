from flask import Blueprint, render_template, request, redirect, flash, session, url_for, Flask
from capaNegocio import controlador_practica as c_practica


practica_bp = Blueprint("practica", __name__, template_folder="templates")


@practica_bp.route("/agregar_practica")
def formulario_agregar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        estudiantes, centro_practicas, jefeInmediatos, semestre_academicos, lineaDesarrollos = c_practica.obtener_datos_agregar()
        return render_template("frm_agregar_practica.html",estudiantes=estudiantes,centro_practicas=centro_practicas,jefeInmediatos=jefeInmediatos,semestre_academicos=semestre_academicos,lineaDesarrollos=lineaDesarrollos)


@practica_bp.route("/guardar_practica", methods=["POST"])
def guardar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_estudiante = int(request.form["estudiante"])
        estado = request.form["estado"]
        id_linea_desarrollo = request.form["lineaDesarrollo"]
        id_semestre_academico = request.form["semestreAcademico"]
        id_jefe_inmediato = request.form["jefeInmediato"]
        informacion_adicional = request.form["informacionAdicional"]
        tipo_practica = request.form["tipo_practica"]
    try:
        mensaje = c_practica.agregar_practica(
            id_estudiante, estado, id_linea_desarrollo, id_semestre_academico, id_jefe_inmediato,
            informacion_adicional, tipo_practica
        )

        flash("Práctica registrada con éxito", "success")
        url = "/practicas"
    except ValueError as e:
        mensaje = str(e)
        flash("Error al registrar la práctica: " + mensaje, "error")
        url = "/agregar_practica"

    return redirect(url)
    

@practica_bp.route("/practicas")
def practicas():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            practicas = c_practica.listar_practicas()
            if isinstance(practicas,list):
                return render_template("practica.html", practicas=practicas)
            else:
                print(str(practicas))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener practicas: {e}")
            return redirect(url_for("inicio.inicio"))


@practica_bp.route("/eliminar_practica", methods=["POST"])
def eliminar_practica_route():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        mensaje = c_practica.eliminar_practica(request.form["id"])
        if mensaje == "Operación realizada con éxito":
            flash(f"Práctica eliminada con éxito", "success")
        else:
            print(mensaje)
            flash(str(mensaje), "error")

        return redirect("/practicas")
    
@practica_bp.route("/eliminar_detalle_practica", methods=["POST"])
def eliminar_detalle_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        detalle_id = request.form["id"]
        practica = request.form["id_practica"]
        
        mensaje = c_practica.eliminar_detalle_practica(detalle_id)

        if mensaje == "Operación realizada con éxito":
            flash("Práctica eliminada con éxito", "success")
            return redirect("/practicas")
        else:
            flash(str(mensaje), "error")
            return redirect("/formulario_editar_practica/"+practica)

        

@practica_bp.route("/formulario_editar_practica/<int:id>")
def editar_practica(id):
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        practica = c_practica.buscar_practica_por_ID(id)
        if practica == []:
            c_practica.eliminar_practica(id)
            flash("Se eliminaron todos los detalles de esta practica pre profesional", "warning")
            return redirect("/practicas")
        centro_practicas, jefeInmediatos, semestre_academicos, lineaDesarrollos = c_practica.obtener_datos_editar()
        return render_template("frm_editar_practica.html", id_practica = id, detallesPracticas=practica, centro_practicas=centro_practicas, jefeInmediatos=jefeInmediatos, semestre_academicos=semestre_academicos, lineaDesarrollos=lineaDesarrollos)



@practica_bp.route("/actualizar_practica", methods=["POST"])
def actualizar_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id_d_practica = request.form.get("id")
        estado = request.form.get("estado")
        id_linea_desarrollo = request.form.get("lineaDesarrollo")
        id_semestre_academico = request.form.get("semestreAcademico")
        id_jefe_inmediato = request.form.get("jefeInmediato")
        informacion_adicional = request.form.get("informacionAdicional")
        tipo_practica = request.form["tipo_practica"]
        mensaje = c_practica.actualizar_practica(id_d_practica, id_linea_desarrollo, id_jefe_inmediato, informacion_adicional, estado, id_semestre_academico, tipo_practica)

        if mensaje == "Operación realizada con éxito":
            flash("Práctica actualizada con éxito", "success")
            url = "/practicas"
        else:
            flash(str(mensaje), "error")
            url = "/formulario_editar_practica/" + str(id_practica)
        return redirect(url)


@practica_bp.route("/actualizar_estado_practica", methods=["POST"])
def actualizar_estado_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        id = request.form["id"]
        estado = request.form["estado"]
        mensaje = c_practica.dar_baja_practica(id, estado)

        if mensaje == "Operación realizada con éxito":
            flash(f"Práctica Actualizada con Exito", "success")
        else:
            flash(str(mensaje), "error")

        return redirect("/practicas")
    

@practica_bp.route("/reporte_practica1")
def formulario_reporte_practica():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            datos,nombres_meses = c_practica.grafico_meses_practica('2023-01-01','2024-07-07')
            print(nombres_meses)
            return render_template("reporte_practica.html", datos=datos, nombres_meses=nombres_meses)   
        except Exception as e:
            flash(str(e), "error")
            return redirect("/practicas")
        
@practica_bp.route("/reporte_practica2")
def formulario_reporte_practica2():
    if "rol" not in session or session["rol"] != "Docente de Apoyo":
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            datos, nombre_estados = c_practica.grafico_estado_practica('2023-01-01', '2023-07-07')
            return render_template("reporte_practica2.html", datos=datos, nombres_estados=nombre_estados)
        except Exception as e:
            flash(str(e), "error")
            return redirect("/practicas")
        