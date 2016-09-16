# -*- coding: utf-8 -*-


import json
from flask import Flask, render_template, request, url_for, redirect, flash

from . import app, db
from .models import Product


@app.route('/db/')
def db():
    db.create_all()
    """
    category = db.Column(db.Unicode(64))
    subcategory = db.Column(db.Unicode(64))
    title = db.Column(db.Unicode(64))
    description = db.Column(db.UnicodeText())
    specs = db.Column(db.UnicodeText())
    price = db.Column(db.Integer)
    stage_price = db.Column(db.Integer)
    image = db.Column(db.Unicode(128))
    """
    prod_test = Product(category='wer', subcategory='sdf')
    db.session.add(prod_test)
    db.session.commit()
    return "DF"


@app.route('/', methods=['GET', 'POST'])
def db_page():
    
    with open('antipark/db.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    if request.method == 'POST':
        req_product = request.form.get('product')
        product = data['products'][req_product]
        len_variations = len(product['variations'])
        variations = []
        for var in product['variations']:
            variations.append((var,
                            len(product['variations'][var]['names'].split(',')),
                            len(product['variations'][var]['chars'].split(','))))

        if request.form['submit'] == 'db-look':
            return render_template('db.html', all_products=data['products'].keys(),
                        len_variations=len_variations,
                        variations=variations,
                        product=product)
        elif request.form['submit'] == 'product-info-page':
            return redirect(url_for('products', req_product=req_product))
    
    else:
        return render_template('db.html', all_products=data['products'].keys())
