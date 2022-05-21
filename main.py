from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cart")
def cart():
    return "<h1>CART</h1>  <a href='/'>На главную</a>"


@app.route("/cart1")
def cart1():
    return "<h1>CART1</h1>  <a href='/'>На главную</a>"




if __name__ == "__main__":
    app.run(debug=True)
