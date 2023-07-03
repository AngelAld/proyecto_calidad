from flask import Blueprint, render_template, request, redirect, flash, url_for, session
import capaNegocio.controlador_usuarios as c_usuarios
usuarios_bp = Blueprint("usuario", __name__, template_folder="templates")

@usuarios_bp.route("/")
def login():
    if 'nombre' in session:
        return redirect(url_for('inicio.inicio')) #
    else:
        return render_template('login.html') #cargar un html

@usuarios_bp.route("/iniciar_sesion" , methods=["POST"])
def iniciar_sesion():
    session.clear()
    usuario = c_usuarios.login(request.form['usuario'], request.form['contraseña'])
    if usuario == None:
        flash("El usuario no existe", "error")
    else:
        if usuario[3]:
            session['id'] = usuario[0]
            session['nombre'] = usuario[2]
            session['rol'] = usuario[6]
            return redirect(url_for('inicio.inicio'))
        else:
            flash("Contraseña incorrecta", "error")
    return redirect(url_for('usuario.login'))

@usuarios_bp.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for('usuario.login'))

@usuarios_bp.route("/perfil")
def perfil():
    if "rol" not in session:
        return redirect(url_for("inicio.inicio"))
    else:
        return render_template('perfil.html')
    
    
@usuarios_bp.route("/actualizar_contrasena", methods=["POST"])
def actualizar_contrasena():
    if "rol" not in session:
        return redirect(url_for("inicio.inicio"))

    if request.method == "POST":
        contrasena_actual = request.form.get('contrasena_actual')
        nueva_contrasena = request.form.get('nueva_contrasena')

        if contrasena_actual == nueva_contrasena:
            flash("La contraseña actual y la nueva contraseña son iguales.", "error")
        else:
            resultado = c_usuarios.actualizar_contrasena(session.get("id"), contrasena_actual, nueva_contrasena)

            if resultado is not None:
                flash("Contraseña actualizada exitosamente.", "success")
            else:
                flash("No se pudo actualizar la contraseña. Usuario no encontrado o contraseña actual incorrecta.", "error")

        return render_template("perfil.html")

    return redirect(url_for("inicio.inicio"))

