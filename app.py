from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# 🔐 CLAVE SEGURA
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# 🔒 CONFIGURACIÓN DE SESIÓN
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,   # 🔥 PRODUCCIÓN
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_PERMANENT=False
)

# 🔑 CONTROL TOTAL (DESDE RENDER)
USUARIO = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "1234")

# 🔒 PROTECCIÓN GLOBAL
@app.before_request
def proteger():

    if request.path == "/" or request.path.startswith("/static"):
        return

    if "usuario" not in session:
        return redirect(url_for("login"))

# 🔐 EVITAR CACHE (CRÍTICO)
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"].strip()
        password = request.form["password"].strip()

        if usuario == USUARIO and password == PASSWORD:
            session.clear()
            session["usuario"] = usuario
            return redirect(url_for("mapa"))
        else:
            return "Acceso denegado"

    return render_template("login.html")

# MAPA
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

