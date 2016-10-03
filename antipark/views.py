# -*- coding: utf-8 -*-

import datetime
import json
import os
from flask import Flask, render_template, request, url_for, redirect, flash, \
                            send_file
from flask_mail import Message

from . import app, db, mail
from .models import Product, Category, Service


all_categories = Category.query.all()
all_goods      = Product.query.all()
all_services   = Service.query.all()


site_url = 'http://antipark.ru/'


@app.route('/')
def index():
    return render_template('index.html', categories=all_categories,
                                         services=all_services)


@app.route('/goods/')
def about():
    return render_template('goods.html', categories=all_categories)


@app.route('/goods-category/<category_id>/')
def goods_category(category_id):
    category = Category.query.get(category_id)
    goods = Product.query.filter_by(category=category_id).all()
    return render_template('goods-category.html', categories=all_categories,
                                category=category, goods=goods)


@app.route('/goods-item/<goods_item_id>/')
def goods_item(goods_item_id):
    goods_item = Product.query.get(str(goods_item_id))
    category_id = goods_item.category
    category = Category.query.get(category_id)
    return render_template('goods-item.html', categories=all_categories,
                                category=category, goods_item=goods_item)


@app.route('/services/')
def services():
    return render_template('services.html', services=all_services,
                                            categories=all_categories)


@app.route('/service-item/<service_item_id>')
def service_item(service_item_id):
    service_item = Service.query.get(str(service_item_id))
    return render_template('service-item.html', service=service_item,
                                            categories=all_categories)


@app.route('/file/')
def file():
    return render_template('file.html', categories=all_categories)


@app.route('/order') # , methods=['POST'])
def orderCall():
    if request.method == 'POST':
        data = request.get_json()
        msg = Message(subject="Заказ товара с сайта Antipark.ru",
                        sender="admin@jokerinteractive.ru",
                        recipients=["igor@auto-res.ru", "admin@z-gu.ru"],
                        charset="utf-8")
        msg.body = "Поля: " + str(data)
        msg.html = '<div style="background-color: #fff; width: 500px;">'
        msg.html += '<p style="color: #fff; background-color: #cd2312; font-size: 24px; padding: 15px 0; text-align: center; margin: 0;">Заказ товара!</p>'
        msg.html += '<div style="padding: 20px 40px 20px 80px;">'
        msg.html += '<p slyle="color: #000; font-size: 18px;">Товар: <strong>' + data['goods'] + '</strong></p>'
        msg.html += '<p slyle="color: #000; font-size: 18px;">Телефон клиента: <strong><a href="tel: "' + data['tel'] + '" style="color: #2fa4e7; text-decoration: none;">' + data['tel'] + '</a></strong></p>'
        msg.html += '<p slyle="color: #000; font-size: 18px;">Email клиента: <strong><a href="email: "' + data['email'] + '" style="color: #2fa4e7; text-decoration: none;">' + data['email'] + '</a></strong></p>'
        msg.html += '<p slyle="color: #000; font-size: 18px;">Время отправки: ' + datetime.datetime.now().ctime() + '</p>'
        msg.html += '<hr>'
        msg.html += '<p slyle="color: #000; font-size: 12px;">Заявка отправлена с сайта <a href="http://antipark.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">antipark.ru</a></p>'
        msg.html += '<p slyle="color: #000; font-size: 12px;">Сайт с любовью сделан студией <a href="https://jokerinteractive.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">jokerinteractive.ru</a></p>'
        msg.html += '</div>'
        msg.html += '</div>'
        mail.send(msg)
        return 'OK'


@app.route('/update_market/')
def update_market():
    import pandas as pd
    import re
    from collections import defaultdict

    price_cols = ['id', 'title', 'price', 'category', 'url', 'currencyId']

    prods = defaultdict(list)
    for col in price_cols:
        for product in all_goods:
            if col == 'url':
                prods[col].append(site_url + 'goods-item/' + str(product.id))
            elif col == 'currencyId':
                prods[col].append('RUR')
            elif col == 'price':
                pr = re.sub('\D', '', getattr(product, col))
                if not pr:
                    pr = '1'
                prods[col].append(pr)
            else:
                prods[col].append(getattr(product, col))

    df = pd.DataFrame(prods)
    df.set_index('id', inplace=True)
    df.rename(columns={'title': 'name'}, inplace=True)
    df.to_excel('database/market.xlsx')

    return 'OK'


@app.route('/save_db/', methods=['POST'])
def save_db():

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Bad'
        file = request.files['file']
        if file.filename == '':
            return 'Bad'
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'database.xlsx'))

            import pandas as pd

            df_new = pd.read_excel('database/database.xlsx', index_col='id')
            
            for prod in df_new.itertuples():
                upd_product = Product.query.get(str(prod.Index))
                for field in prod._fields[1:]:
                    setattr(upd_product, field, getattr(prod, field))
                db.session.commit()
            return 'OK'


@app.route('/get_db/')
def get_db():
    import pandas as pd
    from collections import defaultdict

    price_cols = ['id', 'title', 'price', 'stage_price']

    prods = defaultdict(list)
    for col in price_cols:
        for product in all_goods:
            prods[col].append(getattr(product, col))

    df = pd.DataFrame(prods)
    df.set_index('id', inplace=True)
    df.to_excel('database/database.xlsx')

    f = '../database/database.xlsx'
    return send_file(f, as_attachment=True)
