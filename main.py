from flask import Flask, render_template, url_for, request, redirect
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


@app.route("/cards")
def cards():
    cards_posts = Card.query.order_by(Card.time.desc()).all()
    return render_template("cards.html", cards_posts=cards_posts)


@app.route("/cards/<int:id>")
def cards_detail(id):
    card = Card.query.get(id)
    return render_template("card_detail.html", card=card)


@app.route("/create-card", methods=['POST', 'GET'])
def create_card():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        full_description = request.form['full_description']
        price = request.form['price']
        card = Card(title=title, description=description, full_description=full_description, price=price)

        try:
            db.session.add(card)
            db.session.commit()
            return redirect('/cards')
        except:
            return "При добавлении карточки произошла ошибка"
    else:
        return render_template("create-card.html")



@app.route("/cart1")
def cart1():
    return render_template("cart1.html")


@app.route("/secret_page")
def secret_page():
    return render_template("secret_page.html")


@app.route("/news")
def news():
    news = News.query.order_by(News.time.desc()).all()
    return render_template("news.html", news=news)


@app.route("/news/<int:id>")
def news_detail(id):
    new = News.query.get(id)
    return render_template("news_detail.html", new=new)


@app.route("/create_news", methods=['POST', 'GET'])
def create_news():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        news = News(title=title, intro=intro, text=text)

        try:
            db.session.add(news)
            db.session.commit()
            return redirect('/news')
        except:
            return "При добавлении новости произошла ошибка"
    else:
        return render_template("create_news.html")


if __name__ == "__main__":
    app.run(debug=True)
