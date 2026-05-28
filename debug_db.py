import sqlite3

conn = sqlite3.connect("oficina_do_pombo.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(reparacoes)")
print(cursor.fetchall())

conn.close()