from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glass.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Card %r>' % self.id


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Card %r>' % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create-card")
def create_card():
    return render_template("create-card.html")


@app.route("/cart1")
def cart1():
    return render_template("cart1.html")


@app.route("/secret_page")
def secret_page():
    return render_template("secret_page.html")


@app.route("/create_news")
def create_news():
    return render_template("create_news.html")


if __name__ == "__main__":
    app.run(debug=True)
