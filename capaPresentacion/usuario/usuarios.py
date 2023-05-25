from flask import Blueprint, render_template, request, redirect, flash

usuarios_bp = Blueprint("usuario", __name__, template_folder="templates")

@usuarios_bp.route("/")
def login():
    return render_template('login.html')



@usuarios_bp.route("/iniciar_sesion" , methods=["POST"])
def iniciar_sesion():
    if request.method == 'POST':
        print("a")    
    return redirect('/inicio')