#!/usr/bin/python3

# DB with products looker
# __author__ : vlfedotov

import json
from flask import Flask, render_template, request, url_for, redirect, flash


app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/login/')
def login():
    flash('You were successfully logged in')
    return "Hi"


@app.route('/', methods=['GET', 'POST'])
def db_page():
    
    with open('db.json', encoding='utf-8') as json_file:
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


@app.route('/products/<req_product>/')
def products(req_product):
    with open('db.json') as json_file:
        data = json.load(json_file)

    product = data['products'][req_product]
    len_variations = len(product['variations'])
    variations = []
    for var in product['variations']:
        variations.append((var,
                        len(product['variations'][var]['names'].split(',')),
                        len(product['variations'][var]['chars'].split(','))))

    return render_template('product_info.html',
                                len_variations=len_variations,
                                variations=variations,
                                product=product)


if __name__ == '__main__':
    app.run(port=1234, debug=True)
