# Uses request.args.get

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])    
def index():
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "world"))
    else:
        return render_template("index.html")

@app.route("/greet", methods=["POST", "GET"])
def greet():
    return render_template("greet.html", name=request.form.get("name", "world"))


if __name__ == "__main__":
    app.run(debug=True)