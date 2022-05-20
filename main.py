from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>HELLO WORLD</h1> <a href='about'>Перейди</a>"


@app.route("/about")
def about():
    return "<h1>ABOUT</h1>  <a href='/'>На главную</a>"


@app.route("/cart")
def cart():
    return "<h1>CART</h1>  <a href='/'>На главную</a>"





if __name__ == "__main__":
    app.run(debug=True)
