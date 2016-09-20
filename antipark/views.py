# -*- coding: utf-8 -*-


import json
from flask import Flask, render_template, request, url_for, redirect, flash

from . import app, db
from .models import Product, Category


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

all_categories = Category.query.all()
all_goods      = Product.query.all()

@app.route('/goods/')
def about():
    return render_template('goods.html', categories=all_categories)


@app.route('/goods-item/<category_id>')
def goods_item(category_id):
    category = Category.query.get(category_id)
    goods = Product.query.filter_by(category=category_id).all()
    return render_template('goods-item.html', category=category, goods=goods)


@app.route('/goods-category/')
def goods_category():
    return render_template('goods-category.html', categories=all_categories)


@app.route('/file')
def file():
    return render_template('file.html')
