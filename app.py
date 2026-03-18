@app.route("/mapa")
def mapa():
    if not session.get("logged_in"):
        return redirect("/")
    return "MAPA OK FUNCIONANDO"