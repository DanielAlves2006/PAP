import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for, flash

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


@produtos_route.route('/comprar_produto/<int:id>', methods=['GET', 'POST'])
def comprar_produto(id):
    if 'user_id' not in session:
        flash("Por favor, faça login para comprar produtos.", "warning")
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        metodo_pagamento = request.form.get('metodo_pagamento')
        cliente_id = session.get('user_id')

      
        cursor.execute("SELECT preco FROM produtos WHERE id = ?", (id,))
        preco_prod = cursor.fetchone()

        if preco_prod:
            preco = preco_prod[0]

            
            cursor.execute("""
                INSERT INTO encomendas (cliente_id, total, estado, metodo_pagamento)
                VALUES (?, ?, 'Pendente', ?)
            """, (cliente_id, preco, metodo_pagamento))
            encomenda_id = cursor.lastrowid

            
            cursor.execute("""
                INSERT INTO encomenda_itens (encomenda_id, produto_id, quantidade, preco)
                VALUES (?, ?, 1, ?)
            """, (encomenda_id, id, preco))

            conn.commit()
            conn.close()
            flash("Compra efetuada com sucesso! Aguarde a confirmação de pagamento pelo administrador.", "success")
            return redirect('/produto')

    cursor.execute("""
        SELECT p.id, p.nome, p.descricao, p.preco, p.imagem, c.nome
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (id,))
    produto = cursor.fetchone()
    conn.close()

    if not produto:
        return redirect('/produto')

    return render_template('comprar_produto.html', produto=produto)