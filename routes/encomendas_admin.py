from flask import Blueprint, render_template

encomendas_admin_route = Blueprint('encomendas_admin', __name__)

@encomendas_admin_route.route('/encomenda_admin')
def encomendas_admin():
    return render_template('encomenda_admin.html')