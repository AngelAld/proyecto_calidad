from flask import render_template, request, redirect, flash
import static.python.controladores.controlador_semestres as c_semestres

from __main__ import app


@app.route("/agregar_semestre")
def formulario_agregar_semestre():
    return render_template('semestre/frm_agregar_semestre.html')


@app.route("/guardar_semestre", methods=["POST"])
def guardar_semestre():
    nombre = request.form["nombre"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_fin = request.form["fecha_fin"]
    frm_estado = request.form.get("estado")
    if frm_estado == 'on':
        estado = 'A'
    else:
        estado = 'I'

    mensaje = c_semestres.insert(nombre, fecha_inicio, fecha_fin, estado)

    if mensaje[0] == "Operación realizada con éxito":
        flash(f"Semestre Registrado con Exito", "success")
        url = "/semestres"
    else:
        flash(mensaje[0], "error")
        url = "/agregar_semestre"

    return redirect(url)


@app.route("/")
@app.route("/semestres")
def semestres():
    semestres = c_semestres.getAll()
    return render_template('semestre/semestres.html', semestres=semestres)


def buscar_semestre(p_nombre, p_semestre):
    resultados = []
    for semestre in semestres:
        if p_nombre.lower() in semestre[1].lower():
            resultados.append(semestre)
    return resultados


@app.route("/eliminar_semestre", methods=["POST"])
def eliminar_semestre():

    mensaje = c_semestres.delete(request.form["id"])
    if mensaje[0] == "Operación realizada con éxito":
        flash(f"Semestre Eliminado con Exito", "success")
    else:
        flash(mensaje[0], "error")

    return redirect("/semestres")


@app.route("/formulario_editar_semestre/<int:id>")
def editar_semestre(id):
    # Obtener el semestre por ID
    semestre = c_semestres.getById(id)
    return render_template('semestre/frm_editar_semestre.html', semestre=semestre)


@app.route("/actualizar_semestre", methods=["POST"])
def actualizar_semestre():
    id = request.form["id"]
    nombre = request.form["nombre"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_fin = request.form["fecha_fin"]
    frm_estado = request.form.get("estado")
    if frm_estado == 'on':
        estado = 'A'
    else:
        estado = 'I'

    mensaje = c_semestres.update(id, nombre, fecha_inicio, fecha_fin, estado)

    if mensaje[0] == "Operación realizada con éxito":
        flash(f"Semestre Actualizado con Exito", "success")
        url = "/semestres"
    else:
        flash(mensaje[0], "error")
        url = "/formulario_editar_semestre/"+id

    return redirect(url)


@app.route("/actualizar_estado", methods=["POST"])
def actualizar_estado():
    id = request.form["id"]
    frm_estado = request.form.get("estado")
    if frm_estado == 'on':
        estado = 'A'
    else:
        estado = 'I'
    mensaje = c_semestres.update_estado(id, estado)

    if mensaje[0] == "Operación realizada con éxito":
        flash(f"Semestre Actualizado con Exito", "success")
    else:
        flash(mensaje[0], "error")

    return redirect("/semestres")
