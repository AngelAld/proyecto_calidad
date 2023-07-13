from flask import Flask, Blueprint, render_template, request, redirect, flash, session, url_for
from capaPresentacion.inicio.inicio import inicio_bp
from capaPresentacion.semestre.semestres import semestres_bp
from capaPresentacion.usuario.usuarios import usuarios_bp
from capaPresentacion.lineaDesarrollo.linea_desarrollo import linea_desarrollo_bp
from capaPresentacion.centroPPP.centro_PPP import cPPP_bp
from capaPresentacion.Estudiante.estudiante import estudiante_bp
from capaPresentacion.docenteApoyo.docentes import docentes_bp
from capaPresentacion.facultad.facultades import facultad_bp
from capaPresentacion.escuela_profesional.escuelas import escuela_bp
from capaPresentacion.planEstudio.plan_estudio import plan_estudio_bp
from capaPresentacion.Practica.practica import practica_bp   
from capaPresentacion.informe_inicial_es.informe_inicial_es import informe_inicial_es_bp
from capaPresentacion.informe_inicial_em.informe_inicial_em import informe_inicial_em_bp
from capaPresentacion.ficha_desempeno.ficha_desempeno import ficha_desempeno_bp
from capaPresentacion.informe_final_em.informe_final_em import informe_final_em_bp
from capaPresentacion.informe_final_es.informe_final_es import informe_final_es_bp
from capaPresentacion.Jefe_Inmediato.jefe_inmediato import jefe_inmediato_bp
from capaPresentacion.tituloProfesional.titulo_profesional import titulo_profesional_bp
from capaPresentacion.Reporte_Informes_Finalizados.reporte_informes_finalizados import informes_finales_bp

app = Flask(__name__)
app.secret_key = "nose"
app.register_blueprint(inicio_bp)
app.register_blueprint(semestres_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(linea_desarrollo_bp)
app.register_blueprint(cPPP_bp)
app.register_blueprint(estudiante_bp)
app.register_blueprint(docentes_bp)
app.register_blueprint(facultad_bp)
app.register_blueprint(escuela_bp)
app.register_blueprint(plan_estudio_bp)
app.register_blueprint(practica_bp)
app.register_blueprint(informe_inicial_es_bp)
app.register_blueprint(informe_inicial_em_bp)
app.register_blueprint(ficha_desempeno_bp)
app.register_blueprint(informe_final_em_bp)
app.register_blueprint(informe_final_es_bp)
app.register_blueprint(jefe_inmediato_bp)
app.register_blueprint(titulo_profesional_bp)
app.register_blueprint(informes_finales_bp)


# @app.errorhandler(404)
# def no_encontrado(e):
#     flash('La url solicitada no existe', 'error')
#     return redirect(url_for('inicio.inicio'))
# @app.errorhandler(500)
# def error_500(e):
#     flash('Ha ocurrido un error inesperado!', 'error')
#     return redirect(url_for('inicio.inicio'))


# Iniciar el servidor
if __name__ == "__main__":
    app.config.from_object("config")
    app.config["SESSION_COOKIE_SECURE"] = True
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=True,
        ssl_context=app.config.get("SSL"),
    )
