from flask import Blueprint, render_template

reparacoes_route = Blueprint('reparacoes', __name__)

@reparacoes_route.route('/reparacao_admin')
def reparacoes():
    return render_template('reparacao_admin.html')