from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # 🔥 PRUEBA SIN VALIDACIÓN
        return redirect("/mapa")

    return render_template("login.html")


# MAPA
@app.route("/mapa")
def mapa():
    return "MAPA CARGANDO OK"


if __name__ == "__main__":
    app.run(debug=True)