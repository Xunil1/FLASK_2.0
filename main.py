from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import telebot_our

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glass.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


uploads_dir = os.path.join(app.root_path, 'static\image')

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, default=0)
    img_path = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DateTime, default=datetime.today())


    def __repr__(self):
        return '<Card %r>' % self.id


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    img_path = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<New %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(300), nullable=False)
    surname = db.Column(db.String(300), nullable=False)
    mail = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<User %r>' % self.id


class User_order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    product_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<User_order %r>' % self.id


class Order_from_header(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Order_from_header %r>' % self.id


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


@app.route("/cards/<int:id>/del")
def cards_delete(id):
    card = Card.query.get_or_404(id)
    try:
        db.session.delete(card)
        db.session.commit()
        return redirect('/cards')
    except:
        return "При удалении карточки произошла ошибка"


@app.route("/cards/<int:id>/update", methods=['POST', 'GET'])
def update_card(id):
    card = Card.query.get(id)
    path = uploads_dir + '/' + card.img_path
    if (os.path.isfile(path)):
        os.remove(path)
    if request.method == 'POST':
        card.title = request.form['title']
        card.description = request.form['description']
        card.full_description = request.form['full_description']
        card.price = request.form['price']
        card.img_path = request.files['img'].filename
        request.files['img'].save(os.path.join(uploads_dir, request.files['img'].filename))
        try:
            db.session.commit()
            return redirect('/cards')
        except:
            return "При обновлении карточки произошла ошибка"
    else:
        return render_template("update-card.html", card=card)


@app.route("/create-card", methods=['POST', 'GET'])
def create_card():

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        full_description = request.form['full_description']
        price = request.form['price']
        img = request.files['img']
        img.save(os.path.join(uploads_dir, img.filename))

        card = Card(title=title, description=description, full_description=full_description, price=price, img_path=img.filename)

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


@app.route("/news/<int:id>/delete")
def new_delete(id):
    new = News.query.get_or_404(id)

    try:
        db.session.delete(new)
        db.session.commit()
        return redirect('/news')
    except:
        return "При удалении новости произошла ошибка"


@app.route("/news/<int:id>/update", methods=['POST', 'GET'])
def new_update(id):
    new = News.query.get(id)
    if request.method == 'POST':
        new.title = request.form['title']
        new.intro = request.form['intro']
        new.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/news')
        except:
            return "При редактировани новости произошла ошибка"
    else:
        return render_template("new_update.html", new=new)


@app.route("/create_news", methods=['POST', 'GET'])
def create_news():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        img = request.files['img']
        img.save(os.path.join(uploads_dir, img.filename))

        news = News(title=title, intro=intro, text=text, img_path=img.filename)

        try:
            db.session.add(news)
            db.session.commit()
            return redirect('/news')
        except:
            return "При добавлении новости произошла ошибка"
    else:
        return render_template("create_news.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        mail = request.form['mail']
        phone = request.form['phone']
        password = request.form['password']

        user = User(username=username, name=name, surname=surname, mail=mail, phone=phone, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        except:
            return "При добавлении пользователя произошла ошибка"
    else:
        return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if request.form['password'] == user.password:
            return redirect('/cards')

    else:
        return render_template("login.html")


@app.route("/order/<int:id>", methods=['POST', 'GET'])
def order(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        user_order = User_order(name=name, phone=phone, address=address, product_id=id)
        try:
            db.session.add(user_order)
            db.session.commit()
            order = User_order.query.order_by(User_order.time.desc()).first()
            card = Card.query.get(id)
            to_telegram = {'id': order.id, 'name': order.name, 'phone': order.phone, 'address': order.address, 'product_id': card.id, 'product_name': card.title, 'product_price': card.price}
            telebot_our.send_message(to_telegram)
            return redirect('/')
        except:
            return "При создании заказа произошла ошибка"
    else:
        return render_template("order.html")


@app.route("/order_from_header", methods=['POST', 'GET'])
def order_from_header():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        order_from_header = Order_from_header(name=name, phone=phone, address=address)

        try:
            db.session.add(order_from_header)
            db.session.commit()
            return redirect('/')
        except:
            return "При создании заказа произошла ошибка"

    else:
        return render_template("order_from_header.html")


if __name__ == "__main__":
    app.run(debug=True)


