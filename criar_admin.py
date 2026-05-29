import sqlite3
import hashlib

def criar_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("oficina_do_pombo.db")
cursor = conn.cursor()

senha_hash = criar_hash("ecoeletronicodomundo2026")

cursor.execute("""
INSERT INTO utilizadores(nome, email, senha_hash, tipo)
VALUES (?, ?, ?, ?)
""", ("Administrador", "ecoeletronico2026@gmail.com", senha_hash,"admin"))

conn.commit()
conn.close()

print("Administrador criado com sucesso!")