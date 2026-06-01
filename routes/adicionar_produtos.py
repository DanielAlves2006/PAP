import sqlite3
from flask import Blueprint, render_template, request, redirect, session

adicionar_produtos_route = Blueprint('adicionar_produtos', __name__)

@adicionar_produtos_route.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produtos():
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
        quantidade = int(request.form.get('quantidade', 0))

        cursor.execute("""
            INSERT INTO produtos (nome, descricao, preco, categoria_id, imagem)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, descricao, preco, categoria_id, imagem))
        produto_id = cursor.lastrowid

        # Insert initial stock entry for default store (loja_id = 1)
        cursor.execute("""
            INSERT INTO stock (produto_id, loja_id, quantidade)
            VALUES (?, ?, ?)
        """, (produto_id, 1, quantidade))

        conn.commit()
        conn.close()
        return redirect('/gerir_stock')

    # GET: fetch categories for form select dropdown
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    conn.close()

    return render_template('adicionar_produto.html', categorias=categorias)