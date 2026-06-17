from flask import Blueprint, render_template, request, redirect
from flask_mail import Message
from extensoes import mail
import sqlite3

reparacoes_route = Blueprint('reparacoes', __name__)

@reparacoes_route.route('/reparacao_admin')
def reparacoes():

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        clientes_id,
        equipamento,
        marca,
        modelo,
        problema,
        data_reparacao,
        hora_reparacao,
        estado
    FROM reparacoes
    ORDER BY data_reparacao DESC
    """)

    reparacoes = cursor.fetchall()
    
    conn.close()

    return render_template(
        'reparacao_admin.html',
        reparacoes=reparacoes
    )


@reparacoes_route.route('/atualizar_reparacao/<int:id>', methods=['POST'])
def atualizar_reparacao(id):

    estado = request.form.get('estado')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    # Update database status first
    cursor.execute("""
    UPDATE reparacoes
    SET estado = ?
    WHERE id = ?
    """, (estado, id))
    conn.commit()

    # If the new status is "Concluída", send notification email
    if estado == 'Concluída':
        try:
            # Fetch user email and equipment details
            cursor.execute("""
                SELECT r.equipamento, r.marca, r.modelo, u.email, u.nome
                FROM reparacoes r
                JOIN utilizadores u ON r.clientes_id = u.id_user
                WHERE r.id = ?
            """, (id,))
            info = cursor.fetchone()

            if info:
                equipamento, marca, modelo, user_email, user_name = info
                
                # Check that user email is not null/empty
                if user_email:
                    marca_str = f" {marca}" if marca else ""
                    modelo_str = f" {modelo}" if modelo else ""
                    equip_str = f"{equipamento}{marca_str}{modelo_str}"

                    msg = Message(
                        subject="Oficina do Pombo - Reparação Concluída",
                        sender="ecoeletronico2026@gmail.com",
                        recipients=[user_email],
                        body=f"""Olá {user_name},

Informamos que a reparação do seu equipamento ({equip_str}) foi concluída com sucesso!

Poderá deslocar-se à nossa oficina para efetuar o levantamento do mesmo.

Melhores cumprimentos,
Oficina do Pombo"""
                    )
                    mail.send(msg)
                    print(f"E-mail de conclusão enviado com sucesso para: {user_email}")
        except Exception as e:
            # Log the error, but don't crash the update request
            print(f"Erro ao enviar e-mail de conclusão de reparação: {e}")

    conn.close()

    return redirect('/reparacao_admin')