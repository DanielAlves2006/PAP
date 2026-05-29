from flask import Blueprint, render_template

adicionar_produtos_route = Blueprint('adicionar_produtos', __name__)

@adicionar_produtos_route.route('/adicionar_produto')
def adicionar_produtos():
    return render_template('adicionar_produto.html')