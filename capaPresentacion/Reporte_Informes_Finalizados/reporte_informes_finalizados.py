from flask import Blueprint, render_template, request, redirect, flash, session, url_for,  make_response
from capaNegocio import controlador_informes_finalizados as c_informes_finalizados

informes_finales_bp = Blueprint("informes_finales", __name__, template_folder="templates")

@informes_finales_bp.route("/reporte_informes_finales")
def reporte_informes_finales():
    rol = session.get("rol")
    if not rol or (rol != "Estudiante" and rol != "Docente de Apoyo"):
        return redirect(url_for("inicio.inicio"))
    else:
        try:
            informes_finales = c_informes_finalizados.listar_informes_finalizados()
            if isinstance(informes_finales, list):
                return render_template("informes_finalizados.html", informes_finales=informes_finales)
            else:
                print(str(informes_finales))
                return redirect(url_for("inicio.inicio"))
        except Exception as e:
            print(f"Error al obtener informes finales: {e}")
            return redirect(url_for("inicio.inicio"))
        


