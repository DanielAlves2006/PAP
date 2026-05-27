from flask import Flask
from routes.index import main
from routes.marcas import marcas_route
from routes.produtos import produtos_route
from routes.agendar_reparacoes import agendar_reparacoes_route
from routes.autenticar import autenticar_route
from routes.cadastrar_registro import cadastrar_registro




app = Flask(__name__)

app.secret_key = 'password_qualquer_coisa'

app.register_blueprint(main)
app.register_blueprint(marcas_route)
app.register_blueprint(produtos_route)
app.register_blueprint(agendar_reparacoes_route)
app.register_blueprint(autenticar_route)
app.register_blueprint(cadastrar_registro)

if __name__ == "__main__":
    app.run(debug=True)
