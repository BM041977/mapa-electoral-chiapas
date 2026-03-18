from flask import Flask, render_template, request, redirect, session
import os
from datetime import timedelta

app = Flask(__name__)

# 🔐 CONFIGURACIÓN SEGURA
app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")
app.permanent_session_lifetime = timedelta(minutes=10)

# 🔐 USUARIO Y PASSWORD
USER = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")

# 🔒 EVITAR CACHE (CLAVE)
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        if usuario == USER and password == PASSWORD:
            session.clear()
            session.permanent = False  # 🔥 IMPORTANTE
            session["logged_in"] = True
            return redirect("/mapa")

        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


# -----------------------------
# MAPA (PROTEGIDO)
# -----------------------------
@app.route("/mapa")
def mapa():

    if not session.get("logged_in"):
        return redirect("/")

    return render_template("mapa.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------
# EJECUCIÓN LOCAL
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)