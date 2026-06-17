from flask import Blueprint, render_template, redirect, session, request
import sqlite3
from flask_mail import Message
from extensoes import mail

encomendas_admin_route = Blueprint('encomendas_admin', __name__)

@encomendas_admin_route.route('/encomenda_admin')
def encomendas_admin():
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, u.nome, e.total, e.estado, e.data_encomenda, e.metodo_pagamento, u.email
        FROM encomendas e
        JOIN utilizadores u ON e.cliente_id = u.id_user
        ORDER BY e.data_encomenda DESC
    """)
    encomendas = cursor.fetchall()
    conn.close()

    return render_template('encomenda_admin.html', encomendas=encomendas)


@encomendas_admin_route.route('/confirmar_pagamento/<int:id>', methods=['POST'])
def confirmar_pagamento(id):
    if 'user_id' not in session or session.get('tipo') != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

  
    cursor.execute("""
        UPDATE encomendas
        SET estado = 'Pago'
        WHERE id = ?
    """, (id,))
    conn.commit()

   
    cursor.execute("""
        SELECT u.email, u.nome, e.total
        FROM encomendas e
        JOIN utilizadores u ON e.cliente_id = u.id_user
        WHERE e.id = ?
    """, (id,))
    info = cursor.fetchone()

    if info:
        user_email, user_name, total = info
        if user_email:
            try:
                msg = Message(
                    subject="Oficina do Pombo - Confirmação de Pagamento",
                    sender="ecoeletronico2026@gmail.com",
                    recipients=[user_email],
                    body=f"""Olá {user_name},Confirmamos com sucesso o recebimento do pagamento no valor de 
                    {total}€ referente à sua encomenda #{id}!
                    A sua encomenda está agora a ser processada e será expedida em breve.
                    Melhores cumprimentos,
                    Oficina do Pombo"""
                )
                mail.send(msg)
                print(f"E-mail de confirmação de pagamento enviado para: {user_email}")
            except Exception as e:
                print(f"Erro ao enviar e-mail de confirmação de pagamento: {e}")

    conn.close()
    return redirect('/encomenda_admin')