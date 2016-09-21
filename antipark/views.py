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


@app.route('/goods-category/<category_id>/')
def goods_category(category_id):
    category = Category.query.get(category_id)
    goods = Product.query.filter_by(category=category_id).all()
    return render_template('goods-category.html', category=category, goods=goods)


@app.route('/goods-item/<goods_item_id>/', methods=['GET', 'POST'])
def goods_item(goods_item_id):
    if request.method == 'GET':
        goods_item = Product.query.get(str(goods_item_id))
        category_id = goods_item.category
        category = Category.query.get(category_id)
        return render_template('goods-item.html', category=category,
                                                    goods_item=goods_item)


@app.route('/file/', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        import pandas 

        # вместо cur_base.xlsx нужна ссылка на загружаемый файл
        df_new = pd.read_excel('database/database.xlsx', index_col='id')

        for prod in df_new.itertuples():
            upd_product = Product.query.get(prod.Index)
            for field in prod._fields[1:]:
                setattr(upd_product, field, getattr(prod, field))
            db.session.commit()

        return 'Saved'
    return render_template('file.html')


@app.route('/get_db/', methods=['GET', 'POST'])
def get_db():
    # if request.method == 'POST':
    import pandas as pd
    from collections import defaultdict

    price_cols = ['id', 'title', 'price', 'stage_price']

    prods = defaultdict(list)
    for col in price_cols:
        for product in all_goods:
            prods[col].append(getattr(product, col))    

    df = pd.DataFrame(prods)
    df.set_index('id', inplace=True)
    # только в файл cur_base
    df.to_excel('database/database.xlsx')
    flash('Db is saved')
    return redirect(url_for('file'))
