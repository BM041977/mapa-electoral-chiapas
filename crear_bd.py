import sqlite3

conn = sqlite3.connect("usuarios.db")
c = conn.cursor()

# Crear tabla si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
)
""")

# Insertar solo si no existe (evita borrar todo)
usuarios = [
    ("admin", "chiapas"),
    ("analista", "mapa2026")
]

for u, p in usuarios:
    c.execute("INSERT OR IGNORE INTO usuarios (usuario, password) VALUES (?, ?)", (u, p))

conn.commit()
conn.close()

print("Base de datos lista")