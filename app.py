from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_default")

# 🔐 USUARIO Y PASSWORD (Render o local)
USER = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")

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
# RUN LOCAL
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)