from flask import Flask


app = Flask(__name__, static_url_path=None)
app.secret_key = 'nose'

# esto es un truco para no usar blueprints, los imports que siguen si son necesarios
from capaPresentacion.routes import semestres, inicio


# Iniciar el servidor
if __name__ == "__main__":
    app.config.from_object('config')
    app.static_url_path=app.config.get('STATIC_FOLDER')
    app.static_folder=app.root_path + app.static_url_path

    print('========================')
    print(app.static_folder)
    print(app.static_url_path)
    print('========================')

    app.run(
        host=app.config.get('HOST'),
        port=app.config.get('PORT'),
        debug=True, 
        ssl_context=app.config.get('SSL'))
