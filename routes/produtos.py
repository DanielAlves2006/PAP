from flask import Blueprint, render_template

produtos_route = Blueprint('produtos', __name__)

@produtos_route.route('/produto')
def produtos():
    return render_template('produto.html')