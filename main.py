from flask import Flask
from capaPresentacion.inicio.inicio import inicio_bp
from capaPresentacion.semestre.semestres import semestres_bp
from capaPresentacion.usuario.usuarios import usuarios_bp
from capaPresentacion.lineaDesarrollo.linea_desarrollo import linea_desarrollo_bp
from capaPresentacion.Estudiante.estudiante import estudiante_bp
from capaPresentacion.docenteApoyo.docentes import docentes_bp
from capaPresentacion.centroPPP.centro_PPP import cPPP_bp
from capaPresentacion.facultad.facultades import facultad_bp
from capaPresentacion.escuela_profesional.escuelas import escuela_bp
from capaPresentacion.planEstudio.plan_estudio import plan_estudio_bp
from capaPresentacion.Practica.practica import practica_bp   
from capaPresentacion.informe_inicial_es.informe_inicial_es import informe_inicial_es_bp
from capaPresentacion.informe_inicial_em.informe_inicial_em import informe_inicial_em_bp
from capaPresentacion.ficha_desempeno.ficha_desempeno import ficha_desempeno_bp
from capaPresentacion.informe_final_em.informe_final_em import informe_final_em_bp
from capaPresentacion.informe_final_es.informe_final_es import informe_final_es_bp

app = Flask(__name__, static_url_path=None)
app.secret_key = "nose"
app.register_blueprint(inicio_bp)
app.register_blueprint(semestres_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(linea_desarrollo_bp)
app.register_blueprint(estudiante_bp)
app.register_blueprint(docentes_bp)
app.register_blueprint(facultad_bp)
app.register_blueprint(escuela_bp)
app.register_blueprint(plan_estudio_bp)
app.register_blueprint(cPPP_bp)
app.register_blueprint(practica_bp)
app.register_blueprint(informe_inicial_es_bp)
app.register_blueprint(informe_inicial_em_bp)
app.register_blueprint(ficha_desempeno_bp)
app.register_blueprint(informe_final_em_bp)
app.register_blueprint(informe_final_es_bp)

# Iniciar el servidor
if __name__ == "__main__":
    app.config.from_object("config")
    app.static_url_path = app.config.get("STATIC_FOLDER")
    app.static_folder = app.root_path + str(app.static_url_path)

    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=True,
        ssl_context=app.config.get("SSL"),
    )
