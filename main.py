import static.python.routes.semestres
from flask import Flask

app = Flask(__name__)
app.secret_key = 'nose'

# esto es un truco para no usar blueprints, los imports que siguen si son necesarios


# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
    app.run(ssl_context='adhoc')
