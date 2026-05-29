from flask import Flask
from routes.index import main
from routes.marcas import marcas_route
from routes.produtos import produtos_route
from routes.agendar_reparacoes import agendar_reparacoes_route
from routes.autenticar import autenticar_route
from routes.cadastrar_registro import cadastrar_registro
from routes.contactos_email import contactos_email
import routes.contactos_email
from flask_mail import Mail
from extensoes import mail
from routes.admin import admin_route
from routes.adicionar_produtos import adicionar_produtos_route
from routes.gerir_stocks import gerir_stocks_route
from routes.reparacoes import reparacoes_route
from routes.encomendas_admin import encomendas_admin_route




app = Flask(__name__)

app.secret_key = 'password_qualquer'

app.register_blueprint(main)
app.register_blueprint(marcas_route)
app.register_blueprint(produtos_route)
app.register_blueprint(agendar_reparacoes_route)
app.register_blueprint(autenticar_route)
app.register_blueprint(cadastrar_registro)
app.register_blueprint(contactos_email)
app.register_blueprint(admin_route)
app.register_blueprint(adicionar_produtos_route)
app.register_blueprint(gerir_stocks_route)
app.register_blueprint(reparacoes_route)
app.register_blueprint(encomendas_admin_route)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ecoeletronico2026@gmail.com'
app.config['MAIL_PASSWORD'] = 'ssls sboy cqwh jffu'

mail.init_app(app)

routes.contactos_email.mail = mail

if __name__ == "__main__":
    app.run(debug=True)
