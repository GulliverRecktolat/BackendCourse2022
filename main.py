# internet-shop
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import *


app = Flask("HelloWorld")
engine = create_engine('sqlite:///Shop.db', echo=True)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Shop.db'
Session = sessionmaker(bind=engine)
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "Users"
    username = Column(String(50), primary_key=True)
    password = Column(String(50))


class Goods(db.Model):
    __tablename__ = "Goods"
    title = Column(String(50), primary_key=True)
    price = Column(Numeric(10, 2))
    owner = Column(String(50))


db.create_all()
session = Session()
for user in session.query(Users):
    print(f"username-{user.username}, password-{user.password}")


@app.route("/login/", methods=["GET", "POST"])
@app.route("/login/<message>", methods=["GET", "POST"])
def loginPage(message=None):
    session = Session()
    if request.method == "GET":
        session.close()
        return render_template("login.html", message=message)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        query = session.query(Users)
        user = query.filter(Users.username == username).first()
        session.close()
        if user is None:
            return redirect("/register/Please, register.", code=302)
        if user.password != password:
            return redirect("/login/Incorrect password.", code=302)
        return redirect(f"/personalPage/{username}", code=302)


@app.route("/register/<message>", methods=["GET", "POST"])
@app.route("/register/", methods=["GET", "POST"])
def registrationPage(message=None):
    session = Session()
    if request.method == "GET":
        session.close()
        return render_template("register.html", message=message)

    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        query = session.query(Users)
        if password1 != password2:
            return redirect("/register/You should input same passwords.", code=302)
        if query.filter(Users.username == username).first() is not None:
            return redirect("/register/This username is already taken.", code=302)
        session.add(Users(username=username, password=password1))
        session.commit()
        session.close()
        return redirect(f"/personalPage/{username}", code=302)


@app.route("/personalPage/<user>", methods=["GET", "POST"])
def personalPage(user):
    session = Session()
    goods = session.query(Goods)
    if request.method == "GET":
        session.close()
        return render_template("personalPage.html", user=user, goods=goods.all(), message=None)

    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        print(float(price))
        try:
            price = float(price)
        except:
            return render_template("personalPage.html", user=user, goods=goods,
                                   message="Error: Price should be numeric")
        if goods.filter(Goods.title == title).first() is not None:
            return render_template("personalPage.html", user=user, goods=goods,
                                   message="Error: Product with same name already exist")
        session.add(Goods(title=title, price=price, owner=user))
        session.commit()
        session.close()
        return render_template("personalPage.html", user=user, goods=goods, message=None)



if __name__ == '__main__':
    app.run()


"""
# BackendCourse2022
This is a web aplication "Online shop".
It supports logining and registration. Username and password stored in the table "users" of "shop" database.
When user signed in, he enter personal page, where he can view goods, that are currently on sale.
He also able to sell goods himself. Anoter feature is wishlist - user able to pick goods from the list.
"""