import sqlite3
from flask import Blueprint, render_template, request, redirect, session

lojas_route = Blueprint('lojas', __name__)

@lojas_route.route('/adicionar_loja', methods=['GET', 'POST'])
def adicionar_loja():
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        contacto = request.form.get('contacto')

        if nome and localizacao:
            cursor.execute("""
                INSERT INTO lojas (nome, localizacao, contacto)
                VALUES (?, ?, ?)
            """, (nome, localizacao, contacto))
            conn.commit()
            conn.close()
            return redirect('/adicionar_loja')

    cursor.execute("SELECT id, nome, localizacao, contacto FROM lojas")
    lojas = cursor.fetchall()
    conn.close()

    return render_template('adicionar_loja.html', lojas=lojas)
