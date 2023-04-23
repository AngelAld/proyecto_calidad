from flask import Flask, render_template, request, redirect, flash

import controlador_semestres as c_semestres 

app = Flask(__name__)
app.secret_key = 'nose'


@app.route("/agregar_semestre")
def formulario_agregar_semestre():
    return render_template("agregar_semestre.html")


@app.route("/guardar_semestre", methods=["POST"])
def guardar_semestre():
    nombre = request.form["nombre"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_fin = request.form["fecha_fin"]
    mensaje = c_semestres.insert(nombre, fecha_inicio, fecha_fin)

    flash(mensaje[0])
    redirect("/agregar_semestre")
    if mensaje[0] == "Operación realizada con éxito":
        url = "/semestres"
    else:
        url = "/agregar_semestre"
    
    return redirect(url)

@app.route("/")
@app.route("/semestres")
def semestres():
    semestres = c_semestres.getAll()
    return render_template("semestres.html", semestres=semestres)

@app.route("/eliminar_semestre", methods=["POST"])
def eliminar_semestre():
    mensaje = c_semestres.delete(request.form["id"])
    flash(mensaje[0])
    return redirect("/semestres")


@app.route("/formulario_editar_semestre/<int:id>")
def editar_semestre(id):
    # Obtener el semestre por ID
    semestre = c_semestres.getById(id)
    return render_template("editar_semestre.html", semestre=semestre)


@app.route("/actualizar_semestre", methods=["POST"])
def actualizar_semestre():
    id = request.form["id"]
    nombre = request.form["nombre"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_fin = request.form["fecha_fin"]
    if request.form["estado"] == 'Activo':
        estado = 'A'
    else:
        estado = 'I'
    mensaje = c_semestres.update(id, nombre, fecha_inicio, fecha_fin, estado)
  
    flash(mensaje[0])
    
    if mensaje[0] == "Operación realizada con éxito":
        url = "/semestres"
    else:
        url = "/formulario_editar_semestre/"+id
    
    return redirect(url)
    


# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    #app.run(ssl_context='adhoc')
