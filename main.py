from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABSE_URI']

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
    return render_template("cart1.html")

@app.route("/secret_page")
def secret_page():
    return render_template("secret_page.html")


if __name__ == "__main__":
    app.run(debug=True)
