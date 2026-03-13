from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "clave_super_segura"

# -----------------------------
# RUTA DE LA BASE DE DATOS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")


# -----------------------------
# CONEXIÓN A BASE DE DATOS
# -----------------------------
def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREAR TABLA SI NO EXISTE
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


# Ejecutar al iniciar
crear_tabla()


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
            session["usuario"] = usuario
            return redirect(url_for("mapa"))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")


# -----------------------------
# MAPA
# -----------------------------
@app.route("/mapa")
def mapa():

    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("mapa.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("login"))


# -----------------------------
# INICIAR APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)