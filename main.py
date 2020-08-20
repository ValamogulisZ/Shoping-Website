#!/usr/bin/env python
# Author : Wenda Zhao
# -*- coding: UTF-8 -*-


import os
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import json

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'onesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_flag = 0

# table users(8):
# userID(p-key), username, password, first_name, last_name,
# email, address1, address2, balance
class Users(db.Model):
    __tablename__ = "users"
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    address1 = db.Column(db.Text, nullable=False)
    address2 = db.Column(db.Text)
    balance = db.Column(db.Integer)

    def __init__(self, username, password, first_name, last_name, email, address1, address2, balance):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.balance = balance

    def __repr__(self):
        return f"{self.userID},{self.username},{self.password},{self.first_name},{self.last_name},{self.email},{self.address1},{self.address2},{self.balance}"


# items table (5):
# itemId(p-key), item_name, tag, inventory, price, discount
class Merchandise(db.Model):
    ___tablename__ = "items"

    itemID = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Text, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False, index=True)
    url = db.Column(db.Text, nullable=False)

    def __init__(self, item_name, tag, inventory, price, discount, url):
        self.item_name = item_name
        self.tag = tag
        self.inventory = inventory
        self.price = price
        self.discount = discount
        self.url = url

    def __repr__(self):
        return f"{self.itemID},{self.item_name},{self.tag},{self.inventory}," \
            f"{self.price},{self.discount},{self.url}"


class loginForm(FlaskForm):
    login_username = StringField('Username:', validators=[DataRequired()])
    login_password = PasswordField('Password', validators=[DataRequired()])
    submit_login = SubmitField('Login')


class signupForm(FlaskForm):
    signup_username = StringField('Username:', validators=[DataRequired()])
    signup_password = StringField('Password:', validators=[DataRequired()])
    first_name = StringField('first name:', validators=[DataRequired()])
    last_name = StringField('last name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    address1 = StringField('Address line 1:', validators=[DataRequired()])
    address2 = StringField('Address line 2:', validators=[DataRequired()])
    submit_signup = SubmitField('Sign up')


class checkoutForm(FlaskForm):
    checkout_json = HiddenField('Checkout json string', validators=[DataRequired()])
    submit_checkout = SubmitField('Pay')


# function to add new_account
def new_account():
    db_username = session['signup_username']
    db_password = session['signup_password']
    db_first_name = session['first_name']
    db_last_name = session['last_name']
    db_email = session['email']
    db_address1 = session['address1']
    db_address2 = session['address2']
    db_balance = 1000
    new_item = Users(db_username, db_password, db_first_name, db_last_name,
                     db_email, db_address1, db_address2, db_balance)
    db.session.add(new_item)
    db.session.commit()


def item_info(item_id):
    '''
    input  the id of products, then return a dictionary of it
    :param item_id:
    :return:
    '''
    item = str(Merchandise.query.filter(Merchandise.itemID == item_id).all())[1:-1].split(",")
    item_dic = {
        'item_id':item[0],
        'item_name': item[1],
        'item_tag': item[2],
        'item_inventory': item[3],
        'item_price': item[4],
        'item_discount': item[5],
        'item_url': item[6]
    }
    return item_dic


@app.route('/', methods=['GET', 'POST'])
def home():
    customer = False
    if login_flag == 0:
        customer = ""
        session['customer'] = ""
    elif login_flag==1:
        try:
            customer = session['customer']
        except KeyError:
            print("not login")
    return render_template('home.html', customer=customer)


@app.route('/product', methods=['GET', 'POST'])
def product():
    customer = False
    if login_flag == 0:
        session['customer'] = ""
    elif login_flag ==1:
        try:
            customer = session['customer']
        except KeyError:
            print("not login")

    num = Merchandise.query.count()
    id = []
    name = []
    tag = []
    inventory = []
    price = []
    url = []
    for i in range(0,num):
        id.append(item_info(i+1)['item_id'])
        name.append(item_info(i+1)['item_name'])
        tag.append(item_info(i+1)['item_tag'])
        inventory.append(item_info(i+1)['item_inventory'])
        price.append(item_info(i+1)['item_price'])
        url.append(item_info(i+1)['item_url'])

    return render_template('index.html', customer=customer, id=id, name=name, tag=tag, inventory=inventory,
                           price=price,url=url, num=num)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global login_flag
    session['report']=""
    login_form = loginForm()
    session['customer'] = ''
    if login_form.validate_on_submit():
        session['login_username'] = login_form.login_username.data
        session['login_password'] = login_form.login_password.data
        uid = session['login_username']
        psw = session['login_password']
        try:
            user_check = str(Users.query.filter(Users.username == uid).all())[1:-1].split(",")
            if uid == user_check[1]:
                if psw == user_check[2]:
                    session['customer'] = login_form.login_username.data
                    login_form.login_username = ''
                    login_flag=1
                    session['report'] = "You have login successfully"
                    return redirect(url_for('home'))
                else:
                    session['report'] = "password not correct"
        except IndexError:
            session['report'] = "username not exist"
    return render_template('login.html', login_form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session['report']=""
    session['customer']=""
    signup_form = signupForm()
    if signup_form.validate_on_submit():
        session['signup_username'] = signup_form.signup_username.data
        session['signup_password'] = signup_form.signup_password.data
        session['first_name'] = signup_form.first_name.data
        session['last_name'] = signup_form.last_name.data
        session['email'] = signup_form.email.data
        session['address1'] = signup_form.address1.data
        session['address2'] = signup_form.address2.data
        uid = session['signup_username']
        try:
            user_check = str(Users.query.filter(Users.username == uid).all())[1:-1].split(",")
            if user_check[1] == uid:
                session['report'] = "The user name has been token."
        except IndexError:
            new_account()
            session['report'] = "You have successfully signed in"
            return redirect(url_for('login'))
    return render_template('signup.html', signup_form=signup_form)


@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
    customer = session['customer']
    checkout_form = checkoutForm()
    if checkout_form.validate_on_submit():
        session['checkout_json'] = checkout_form.checkout_json.data
        checkout_json = session['checkout_json']
        checkout_dic = json.loads(checkout_json)
        checkout_sum = 0

        for i in range(len(checkout_dic)):
            checkout_sum += float(item_info(checkout_dic[i]['id'])['item_price']) * int(checkout_dic[i]['qty'])
            print(checkout_dic[i]['id'])
            print(item_info(checkout_dic[i]['id'])['item_inventory'])
            new_inventory = int(item_info(checkout_dic[i]['id'])['item_inventory']) - int(checkout_dic[i]['qty'])
            change_item = Merchandise.query.get(checkout_dic[i]['id'])
            change_item.inventory = new_inventory
            db.session.add(change_item)
            db.session.commit()

        account = session['customer']
        new_balance = float(str(Users.query.filter(Users.username == account).all())[1:-1].split(",")[8]) - checkout_sum
        change_user = Users.query.get(str(Users.query.filter(Users.username == account).all())[1:-1].split(",")[0])
        change_user.balance = new_balance
        db.session.add(change_user)
        db.session.commit()
        session['report'] = "The products in your cart have been paid"
        return redirect(url_for('product'))
    return render_template('checkout.html', checkout_form=checkout_form, customer=customer)


@app.route('/discount')
def discount():
    try:
        customer = session['customer']
    except KeyError:
        print("not login")
    finally:
        max_num = Merchandise.query.count()
        num = len(Merchandise.query.filter(Merchandise.discount<1).all())
        id = []
        name = []
        tag = []
        inventory = []
        price = []
        url = []
        for i in range(0, max_num):
            if float(item_info(i+1)['item_discount'])<1:
                id.append(item_info(i + 1)['item_id'])
                name.append(item_info(i + 1)['item_name'])
                tag.append(item_info(i + 1)['item_tag'])
                inventory.append(item_info(i + 1)['item_inventory'])
                price.append(item_info(i + 1)['item_price'])
                url.append(item_info(i + 1)['item_url'])
    return render_template('discount.html',customer=customer, num=num, id=id, name=name, tag=tag,
                           inventory=inventory, price=price, url=url)


if __name__ == '__main__':
    app.run(debug=True)
