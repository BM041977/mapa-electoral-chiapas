from flask import Flask, render_template, request, redirect, session, jsonify
import os
import json
from datetime import timedelta

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")

# ⏳ SESIÓN DE 3 MINUTOS
app.permanent_session_lifetime = timedelta(minutes=3)

# 👤 PROPIETARIO
OWNER = "Baldemar Maza León"

# 🔐 USUARIO Y PASSWORD
USER = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")

# 🔒 EVITAR CACHE
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

    # 🔴 SIEMPRE PEDIR LOGIN
    session.clear()

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        if usuario == USER and password == PASSWORD:

            session["logged_in"] = True
            session.permanent = False

            return redirect("/mapa")

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
        )

    return render_template("login.html")

# -----------------------------
# MAPA
# -----------------------------
@app.route("/mapa")
def mapa():

    if not session.get("logged_in"):
        return redirect("/")

    return render_template("mapa_ligero 1.html")

# -----------------------------
# GEOJSON
# -----------------------------
@app.route("/geojson/secciones")
def geojson_secciones():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "secciones_simplificado.geojson")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)