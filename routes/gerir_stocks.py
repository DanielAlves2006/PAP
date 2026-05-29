from flask import Blueprint, render_template

gerir_stocks_route = Blueprint('gerir_stocks', __name__)

@gerir_stocks_route.route('/gerir_stock')
def gerir_stocks():
    return render_template('gerir_stock.html')