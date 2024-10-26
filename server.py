from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    with open("output/index.html", "r") as index:
        return index.read()


@app.route("/favicon.png")
def favicon():
    with open("output/favicon.png", "rb") as favico:
        return favico.read()


@app.route("/bdir.apk")
def main():
    with open("output/bdir.apk", "rb") as apkfile:
        return apkfile.read()


app.run(host="0.0.0.0", port=1920)
