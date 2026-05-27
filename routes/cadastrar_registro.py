from flask import Blueprint, render_template

cadastrar_registro= Blueprint("cadastrar_registro", __name__)

@cadastrar_registro.route("/cadastro")
def main():
    return render_template("cadastro.html")