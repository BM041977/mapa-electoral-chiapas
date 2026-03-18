from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "clave_super_segura"

# 🔐 Configuración de sesión
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # LOCAL (en Render cambiar a True)

# -----------------------------
# BASE DE DATOS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# CREAR TABLA
# -----------------------------
def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# CREAR USUARIO
# -----------------------------
def crear_usuario():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios")  # 🔥 elimina cualquier usuario anterior

    cursor.execute(
        "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
        ("Baldemar", "Victoria@Ever")
    )

    conn.commit()
    conn.close()

crear_tabla()
crear_usuario()

# -----------------------------
# 🔥 PROTECCIÓN TOTAL
# -----------------------------
@app.before_request
def proteger():
    ruta = request.path

    # Permitir login y archivos estáticos
    if ruta == "/" or ruta.startswith("/static"):
        return

    # Bloquear TODO si no hay sesión
    if "usuario" not in session:
        return redirect("/")

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND password=?",
            (usuario, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session.clear()
            session["usuario"] = usuario
            return redirect("/mapa")
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")

# -----------------------------
# MAPA
# -----------------------------
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)