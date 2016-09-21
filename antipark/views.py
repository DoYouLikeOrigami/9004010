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


@app.route('/file/', methods = ['GET', 'POST'])
def file():
    if request.method == 'POST':
        import pandas 

        # вместо cur_base.xlsx нужна ссылка на загружаемый файл
        df_new = pd.read_excel('cur_base.xlsx', index_col='id')

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
    df.to_excel('cur_base.xlsx')
    flash('Db is saved')
    return redirect(url_for('file'))
