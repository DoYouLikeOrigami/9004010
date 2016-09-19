# -*- coding: utf-8 -*-
__author__ = 'JokerInteractive'
__email__ = 'info@jokerinteractive.ru'

from . import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    # alias = db.Column(db.Unicode(100))
    category = db.Column(db.Unicode(64))
    description = db.Column(db.UnicodeText())

    def __unicode__(self):
        return self.category


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    # alias = db.Column(db.Unicode(100))
    category = db.Column(db.Integer, db.ForeignKey(Category.id))
    subcategory = db.Column(db.Unicode(64))
    title = db.Column(db.Unicode(64))
    specs = db.Column(db.UnicodeText())
    price = db.Column(db.Unicode(10))
    stage_price = db.Column(db.Unicode(10))
    image = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.title
