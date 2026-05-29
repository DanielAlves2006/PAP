import sqlite3
import hashlib 

def criar_hash_senha(password):
    return hashlib.sha256(password.encode()).hexdigest()
    
conn = sqlite3.connect('oficina_do_pombo.db')
conn.execute("PRAGMA FOREIGN_KEYS = ON")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS utilizadores (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    tipo TEXT DEFAULT 'normal'
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS lojas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    localizacao TEXT NOT NULL,
    contacto TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    categoria_id INTEGER,
    imagem TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    loja_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    morada TEXT,
    telefone TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS encomendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_encomenda DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL,
    estado TEXT DEFAULT 'Pendente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS encomenda_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encomenda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY (encomenda_id) REFERENCES encomendas(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS reparacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clientes_id INTEGER NOT NULL,
    equipamento TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    problema TEXT NOT NULL,
    data_reparacao TEXT NOT NULL,
    hora_reparacao TEXT NOT NULL,
    estado TEXT DEFAULT 'Pendente',
    FOREIGN KEY (clientes_id) REFERENCES utilizadores(id_user)
)
""")

conn.commit()

print("Base de dados criada com sucesso!")

conn.close()