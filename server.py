from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    with open("index.html", "r") as index:
        return index.read()


@app.route("/favicon.png")
def favicon():
    with open("favicon.png", "rb") as favico:
        return favico.read()


@app.route("/index.apk")
def main():
    with open("index.apk", "rb") as apkfile:
        return apkfile.read()


app.run(host="0.0.0.0", port=80)
