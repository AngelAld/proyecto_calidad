from flask import Blueprint, render_template, request, redirect, flash

inicio_bp = Blueprint("inicio", __name__, template_folder="templates")


@inicio_bp.route("/inicio")
def inicio():
    return render_template('inicio.html')


