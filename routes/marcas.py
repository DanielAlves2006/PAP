from flask import Blueprint, render_template

marcas_route = Blueprint('marcas', __name__)

@marcas_route.route('/marca')
def marcas():
    return render_template('marca.html')