<<<<<<< HEAD
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
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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
=======
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_segura_123"

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND password=?",
            (usuario, password)
        )

        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            session["usuario"] = usuario
            return redirect("/mapa")

    return render_template("login.html")


# MAPA
@app.route("/mapa")
def mapa():

    if "usuario" not in session:
        return redirect("/")

    return render_template("mapa.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
>>>>>>> 30033d8672c06a82b898483f64a13b7fd6016e39
    app.run(debug=True)