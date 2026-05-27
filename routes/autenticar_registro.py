import sqlite3
from oficina_pombo2 import criar_hash_senha 


def registrar_usuario(nome, email, senha, tipo):

    conn = sqlite3.connect("oficina_do_pombo.db")
    cursor = conn.cursor()

    try:
        senha_hash = criar_hash_senha(senha)

        cursor.execute("""
        INSERT INTO utilizadores(nome, email, senha_hash, tipo)
        VALUES(?, ?, ?, ?)
        """, (nome, email, senha_hash, tipo))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def verificar_login(email, senha):

    conn = sqlite3.connect("oficina_do_pombo.db")
    cursor = conn.cursor()

    senha_hash = criar_hash_senha(senha)

    cursor.execute("""
    SELECT id_user, nome, tipo
    FROM utilizadores
    WHERE email = ? AND senha_hash = ?
    """, (email, senha_hash))

    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'id_user': user[0],
            'nome': user[1],
            'tipo': user[2]
        }

    return None