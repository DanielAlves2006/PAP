from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from routes.autenticar_registro import registrar_usuario, verificar_login

autenticar_route = Blueprint('autenticar', __name__)

@autenticar_route.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo', 'cliente')

        if registrar_usuario(nome, email, senha, tipo):
            return redirect(url_for('autenticar.login'))

        return render_template("cadastrar.html")

    return render_template("cadastrar.html")

@autenticar_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')

        user = verificar_login(email, senha)

        if user:
            session['user_id'] = user['id_user']
            session['nome'] = user['nome']
            session['tipo'] = user['tipo']

            return redirect(url_for('main.index'))

        return render_template("login.html")

    return render_template("login.html")

@autenticar_route.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))        