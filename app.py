from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "OK FUNCIONANDO"

@app.route("/mapa")
def mapa():
    return "MAPA OK"

if __name__ == "__main__":
    app.run(debug=True)