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


@app.route('/goods-item/')
def goods_item():
    return render_template('goods-item.html', goods=all_goods)


@app.route('/goods-category/')
def goods_category():
    return render_template('goods-category.html', categories=all_categories)


@app.route('/file')
def file():
    return render_template('file.html')
