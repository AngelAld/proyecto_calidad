from flask import Blueprint, render_template, request, redirect, flash, url_for
import capaNegocio.controlador_usuarios as c_usuarios
usuarios_bp = Blueprint("usuario", __name__, template_folder="templates")

@usuarios_bp.route("/")
def login():
    return render_template('login.html')

@usuarios_bp.route("/iniciar_sesion" , methods=["POST"])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = c_usuarios.login(request.form['usuario'], request.form['contraseña'])
        if usuario == None:
            flash("El usuario no existe", "error")
        else:
            if usuario[4]:
                return redirect(url_for('inicio.inicio'))
            else:
                flash("Contraseña incorrecta", "error")
    return redirect(url_for('usuario.login'))