<<<<<<< HEAD
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

# Borrar usuarios anteriores (opcional para evitar duplicados)
c.execute("DELETE FROM usuarios")

# Insertar usuarios
c.execute("INSERT INTO usuarios (usuario,password) VALUES ('admin','chiapas')")
c.execute("INSERT INTO usuarios (usuario,password) VALUES ('analista','mapa2026')")

conn.commit()
conn.close()

print("Base de datos creada correctamente")
=======
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
>>>>>>> 30033d8672c06a82b898483f64a13b7fd6016e39
