from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# 🔐 CLAVE SECRETA (desde Render o local)
app.secret_key = os.environ.get("SECRET_KEY", "clave_local_segura")

# 🔑 USUARIO Y PASSWORD (desde Render o local)
USER = os.environ.get("APP_USER", "Baldemar")
PASSWORD = os.environ.get("APP_PASSWORD", "Victoria@Ever")


# -------------------------------------------------
# NO CACHE (para que no se vea el mapa al regresar)
# -------------------------------------------------
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# -------------------------------------------------
# PROTEGER TODAS LAS RUTAS
# -------------------------------------------------
@app.before_request
def proteger():

    # permitir login y archivos estáticos
    if request.path == "/" or request.path.startswith("/static"):
        return

    # si no ha iniciado sesión
    if not session.get("logged_in"):
        return redirect(url_for("login"))


# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        # VALIDACIÓN
        if usuario == USER and password == PASSWORD:
            session.clear()
            session["logged_in"] = True
            return redirect("/mapa")

        return "Usuario o contraseña incorrectos"

    return render_template("login.html")


# -------------------------------------------------
# MAPA (protegido)
# -------------------------------------------------
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------------------------------
# EJECUCIÓN LOCAL
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
