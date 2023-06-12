from flask import Flask
from capaPresentacion.inicio.inicio import inicio_bp
from capaPresentacion.semestre.semestres import semestres_bp
from capaPresentacion.usuario.usuarios import usuarios_bp
from capaPresentacion.informe_inicial_es.informes_inicial_es import informe_inicial_es_bp
from capaPresentacion.informe_inicial_em.informes_inicial_em import informe_inicial_em_bp

app = Flask(__name__, static_url_path=None)
app.secret_key = "nose"
app.register_blueprint(inicio_bp)
app.register_blueprint(semestres_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(informe_inicial_es_bp)
app.register_blueprint(informe_inicial_em_bp)

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

#Comentario para pushear
#aldana malo
