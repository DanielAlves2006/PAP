from flask import Blueprint, render_template

agendar_reparacoes_route = Blueprint('agendar_reparacoes', __name__)

@agendar_reparacoes_route.route('/agendar_reparacao')
def agendar_reparacao():
    return render_template('agendar_reparacao.html')