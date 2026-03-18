from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "clave_super_segura"

# 🔒 NO CACHE
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 🔒 PROTECCIÓN
@app.before_request
def proteger():

    if request.path == "/" or request.path.startswith("/static"):
        return

    if not session.get("logged_in"):
        return redirect(url_for("login"))

# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        if usuario == "Baldemar" and password == "Victoria@Ever":
            session.clear()
            session["logged_in"] = True
            return redirect("/mapa")

        return "Usuario o contraseña incorrectos"

    return "LOGIN FUNCIONANDO OK"

# 🗺️ MAPA
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
