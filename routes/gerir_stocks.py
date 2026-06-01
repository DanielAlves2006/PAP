import sqlite3
from flask import Blueprint, render_template, request, redirect, session

gerir_stocks_route = Blueprint('gerir_stocks', __name__)

@gerir_stocks_route.route('/gerir_stock', methods=['GET', 'POST'])
def gerir_stocks():
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        produto_id = int(request.form.get('produto_id'))
        quantidade = int(request.form.get('quantidade', 0))

        cursor.execute("UPDATE stock SET quantidade = ? WHERE produto_id = ? AND loja_id = 1", (quantidade, produto_id))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO stock (produto_id, loja_id, quantidade) VALUES (?, 1, ?)", (produto_id, quantidade))

        conn.commit()

    cursor.execute("""
        SELECT p.id, p.nome, p.preco, s.quantidade, c.nome AS categoria_nome
        FROM produtos p
        LEFT JOIN stock s ON p.id = s.produto_id
        LEFT JOIN categorias c ON p.categoria_id = c.id
    """)
    produtos = cursor.fetchall()
    conn.close()

    return render_template('gerir_stock.html', produtos=produtos)


@gerir_stocks_route.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        imagem = request.form.get('imagem')
        categoria_id = int(request.form.get('categoria_id'))

        cursor.execute("""
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, categoria_id = ?, imagem = ?
            WHERE id = ?
        """, (nome, descricao, preco, categoria_id, imagem, id))
        conn.commit()
        conn.close()
        return redirect('/gerir_stock')

    cursor.execute("SELECT id, nome, descricao, preco, categoria_id, imagem FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()

    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    conn.close()

    if not produto:
        return redirect('/gerir_stock')

    return render_template('editar_produto.html', produto=produto, categorias=categorias)


@gerir_stocks_route.route('/eliminar_produto/<int:id>', methods=['GET'])
def eliminar_produto(id):
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stock WHERE produto_id = ?", (id,))
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    return redirect('/gerir_stock')


@gerir_stocks_route.route('/eliminar_produtos', methods=['POST'])
def eliminar_produtos():
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    produto_ids = request.form.getlist('produto_ids')
    if not produto_ids:
        return redirect('/gerir_stock')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    try:
        ids = [int(pid) for pid in produto_ids]
    except ValueError:
        conn.close()
        return redirect('/gerir_stock')

    if ids:
        placeholders = ','.join('?' for _ in ids)
        cursor.execute(f"DELETE FROM stock WHERE produto_id IN ({placeholders})", ids)
        cursor.execute(f"DELETE FROM produtos WHERE id IN ({placeholders})", ids)
        conn.commit()

    conn.close()
    return redirect('/gerir_stock')