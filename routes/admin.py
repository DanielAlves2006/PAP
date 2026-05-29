from flask import Blueprint, render_template, session, redirect
import sqlite3

admin_route = Blueprint('admin', __name__)

@admin_route.route('/admin')
def admin():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('tipo') != 'admin':
        return redirect('/')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT produtos.id,
           produtos.nome,
           produtos.preco,
           stock.quantidade
    FROM produtos
    LEFT JOIN stock ON produtos.id = stock.produto_id
    """)

    produtos = cursor.fetchall()

    conn.close()

    return render_template('admin.html', produtos=produtos)