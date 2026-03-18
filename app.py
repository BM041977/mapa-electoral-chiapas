from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# 🔐 CLAVE SECRETA
app.secret_key = "clave_super_segura"

# 🔐 USUARIO Y CONTRASEÑA (FIJOS)
USER = "Baldemar"
PASSWORD = "Victoria@Ever"

# 🔒 NO CACHE (evita ver mapa con botón atrás)
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔒 PROTECCIÓN GLOBAL
@app.before_request
def proteger():

    if request.path == "/" or request.path.startswith("/static"):
        return

    if not session.get("logged_in"):
        return redirect(url_for("login"))

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
            return redirect(url_for("mapa"))
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
    return redirect(url_for("login"))

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
