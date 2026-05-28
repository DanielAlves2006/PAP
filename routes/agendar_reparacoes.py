from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from flask_mail import Message
from extensoes import mail

agendar_reparacoes_route = Blueprint('agendar_reparacoes', __name__)

@agendar_reparacoes_route.route('/agendar_reparacao', methods=['GET', 'POST'])
def agendar_reparacao():

    if request.method == 'POST':

        equipamento = request.form.get('equipamento')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        problema = request.form.get('problema')
        data = request.form.get('data')
        hora = request.form.get('hora')

        clientes_id = session.get('user_id')

        conn = sqlite3.connect('oficina_do_pombo.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reparacoes
        (clientes_id, equipamento, marca, modelo, problema, data_reparacao, hora_reparacao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            clientes_id, equipamento, marca, modelo, problema, data, hora
        ))

        cursor.execute("SELECT email FROM utilizadores WHERE id_user=?", (clientes_id,))
        mail_cliente = cursor.fetchone()[0]

        conn.commit()
        conn.close()

      
        msg = Message(
            subject="A sua reparação foi agendada com sucesso - Oficina do Pombo",
            sender="ecoeletronico2026@gmail.com",
            recipients=[mail_cliente,"ecoeletronico2026@gmail.com"]  
        )

        msg.body = f"""
        Nova reparação agendada:
        Equipamento: {equipamento}
        Marca: {marca}
        Modelo: {modelo}
        Problema: {problema}
        Data: {data}
        Hora: {hora}
        """

        mail.send(msg)

        return redirect('/')

    return render_template('agendar_reparacao.html')