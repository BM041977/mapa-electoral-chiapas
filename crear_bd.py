import sqlite3

conn = sqlite3.connect("usuarios.db")

c = conn.cursor()

c.execute("""
CREATE TABLE usuarios (
id INTEGER PRIMARY KEY,
usuario TEXT,
password TEXT
)
""")

c.execute("INSERT INTO usuarios (usuario,password) VALUES ('admin','chiapas')")
c.execute("INSERT INTO usuarios (usuario,password) VALUES ('analista','mapa2026')")

conn.commit()
conn.close()

print("Base de datos creada")