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
    app.run(debug=True)