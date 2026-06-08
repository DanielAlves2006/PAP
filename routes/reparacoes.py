from flask import Blueprint, render_template, request, redirect
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
def atualizar_reparacao():

    estado = request.form.get('estado')

    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE reparacoes
    SET estado = ?
    WHERE id = ?
    """, (estado, id))

    conn.commit()
    conn.close()

    return redirect('/reparacao_admin')