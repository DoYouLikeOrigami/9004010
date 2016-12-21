# -*- coding: utf-8 -*-
__author__ = 'JokerInteractive'
__email__ = 'info@jokerinteractive.ru'

from datetime import datetime
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(100))
    last_name = db.Column('last_name', db.Unicode(100))
    username = db.Column('username', db.Unicode(80), unique=True, index=True)
    email = db.Column('email', db.Unicode(120), unique=True, index=True)
    password = db.Column(db.Unicode(100))
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return '<User %r>' % (self.username)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    # alias = db.Column(db.Unicode(100))
    category = db.Column(db.Unicode(64))
    description = db.Column(db.UnicodeText())

    def __str__(self):
        return self.category


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    # alias = db.Column(db.Unicode(100))
    category = db.Column(db.Integer, db.ForeignKey(Category.id))
    subcategory = db.Column(db.Unicode(64))
    title = db.Column(db.Unicode(64))
    attr = db.Column(db.Unicode(64))
    specs = db.Column(db.UnicodeText())
    price = db.Column(db.Unicode(10))
    stage_price = db.Column(db.Unicode(10))
    image = db.Column(db.Unicode(128))

    def __str__(self):
        return self.title


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    # alias = db.Column(db.Unicode(100))
    name  = db.Column(db.Unicode(64))
    image = db.Column(db.Unicode(128))
    text  = db.Column(db.UnicodeText())

    def __str__(self):
        return self.category
