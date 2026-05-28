from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message

contactos_email = Blueprint('contactos_email', __name__)

mail = None  

@contactos_email.route('/contactos')
def contactos():
    return render_template('contactos.html')


@contactos_email.route('/enviar_email', methods=['POST'])
def enviar_email():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    mensagem = request.form.get('mensagem', '').strip()

    
    if not nome or not email or not mensagem:
        flash("Por favor, preencha todos os campos.", "warning")
        return redirect(url_for('contactos_email.contactos'))

    try:
        msg = Message( subject=f"Mensagem de contacto - {nome}", sender=email, recipients=['ecoeletronico2026@gmail.com'],  
        body=f"""Nome: {nome} Email: {email} Mensagem: {mensagem}""") 
        mail.send(msg)

        flash("Mensagem enviada com sucesso!", "success")

    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        flash("Erro ao enviar mensagem.", "danger")

    return redirect(url_for('main.index'))