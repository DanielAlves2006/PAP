import sqlite3
from flask import Blueprint, render_template, request

produtos_route = Blueprint('produtos', __name__)

@produtos_route.route('/produto')
def produtos():
    search_query = request.args.get('search', '')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    if search_query:
        cursor.execute("""
            SELECT p.id, p.nome, p.descricao, p.preco, p.imagem, c.nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nome LIKE ?
        """, (f"%{search_query}%",))
    else:
        cursor.execute("""
            SELECT p.id, p.nome, p.descricao, p.preco, p.imagem, c.nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """)

    produtos = cursor.fetchall()
    conn.close()

    return render_template('produto.html', produtos=produtos, search_query=search_query)