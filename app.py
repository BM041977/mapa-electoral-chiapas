from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# 🔐 CLAVE SECRETA (desde Render)
app.secret_key = os.environ.get("SECRET_KEY", "clave_default")

# 🔐 CONFIGURACIÓN DE SESIÓN
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True

# 🚫 EVITAR CACHE (CLAVE PARA SEGURIDAD)
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔑 USUARIO Y PASSWORD (desde Render)
USER = os.environ.get("APP_USER", "admin")
PASSWORD = os.environ.get("APP_PASSWORD", "1234")

# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username")
        password = request.form.get("password")

        if usuario == USER and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("mapa"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

# -------------------------
# MAPA (PROTEGIDO)
# -------------------------
@app.route("/")
def mapa():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("mapa.html")

# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
