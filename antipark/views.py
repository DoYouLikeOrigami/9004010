# -*- coding: utf-8 -*-

import datetime
import json
import os
from flask import Flask, render_template, request, url_for, redirect, flash, send_file, g, make_response
from flask_mail import Message
from flask_login import login_user, logout_user, current_user, login_required

from . import app, db, mail, login_manager
from .models import User, Product, Category, Service


all_goods      = Product.query.all()
all_services   = Service.query.all()

login_manager.login_view = 'login'

site_url = 'http://9004010.ru/'


@app.before_first_request
def init_request():
	db.create_all()


@app.before_request
def before_request():
	g.keys = {
		"3" : "stolbik-kupit-cena-parkovochnyj-dorozhnyj-plastikovyj.html",
		"12" : "vazon-betonnyj-kupit-cena-dlja-cvetov.html",
		"5" : "urna-betonnaya-kupit-cena-dlja-musora.html",
		"13" : "skameyka-betonnaya-kupit-cena-parkovaya-sadovaya-lavka.html",
		"8" : "polusfera-betonnaya-kupit-cena-parkovochnaja-dorozhnaja.html",
		"4" : "konus-kupit-cena-parkovochnyj-dorozhnyj-signalnyj.html",
		"9" : "barjer-kupit-cena-parkovochnyj-skladnoy.html"
		}
	g.all_categories = Category.query.all()
	g.znaki_keys = ["", "Размер знака", "Маска", "Тип А (5 лет)", "Тип А (7 лет)", "Тип Б (10 лет)"]

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if not current_user.is_authenticated:
		return render_template('index.html', categories=g.all_categories, services=all_services)

	if request.method == 'GET':
		return render_template('register.html')

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		email = request.form['email']

		user = User.query.filter_by(username=username)
		print(user)
		if user.count() == 0:
			user = User(username=username, password=password, email=email)
			print('here')
			db.session.add(user)
			db.session.commit()

			flash('Вы зарегистрировались в системе под пользователем {0}. Войдите, пожалуйста.'.format(username))
			return redirect(url_for('login'))
		else:
			flash('Это имя пользователя {0} уже используется. Пожалуйста, выберите дугое.'.format(username))
			return redirect(url_for('register'))

	else:
		abort(405)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', goods=all_goods, categories=g.all_categories)

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		remember_me = False
		if 'remember_me' in request.form:
			remember_me = True

		user = User.query.filter_by(username=username, password=password).first()

		if user is None:
			flash('Имя пользователя или пароль неверный.', 'error')
			return redirect(url_for('login'))

		login_user(user, remember=remember_me)

		flash('Добро пожаловать, {0}!'.format(username))
		return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/')
def index():
	return render_template('index.html', categories=g.all_categories,
										 services=all_services)

@app.route('/bank/')
def bank():
	return render_template('bank.html', categories=g.all_categories)


@app.route('/delivery/')
def delivery():
	return render_template('delivery.html', categories=g.all_categories)


@app.route('/contacts/')
def contacts():
	return render_template('contacts.html', categories=g.all_categories)


@app.route('/blog/')
def blog():
	return render_template('blog.html', categories=g.all_categories)


@app.route('/blog/article/1')
def article1():
	return render_template('article1.html', categories=g.all_categories)


@app.route('/blog/article/2')
def article2():
	return render_template('article2.html', categories=g.all_categories)


@app.route('/blog/article/3')
def article3():
	return render_template('article3.html', categories=g.all_categories)


@app.route('/blog/article/4')
def article4():
	return render_template('article4.html', categories=g.all_categories)


@app.route('/goods/')
def about():
	return render_template('goods.html', categories=g.all_categories)


@app.route('/<alias>/')
@app.route('/goods-category/<number>/')
def alias(alias=None, number=None):
	for key, value in g.keys.items():
		if (value == alias):
			category_id = key
			category = Category.query.get(category_id)
			goods = Product.query.filter_by(category=category_id).all()
			return render_template('goods-category.html', categories=g.all_categories, category=category, goods=goods)

	if number:
		category = Category.query.get(number)
		goods = Product.query.filter_by(category=number).all()

		if (number == "16"):
			return render_template('znaki.html', categories=g.all_categories, category=category, goods=goods, keys=g.znaki_keys)

		return render_template('goods-category.html', categories=g.all_categories, category=category, goods=goods)


@app.route('/goods-item/<goods_item_id>/')
def goods_item(goods_item_id):
	goods_item = Product.query.get(str(goods_item_id))
	category_id = goods_item.category
	category = Category.query.get(category_id)
	return render_template('goods-item.html', categories=g.all_categories,
								category=category, goods_item=goods_item, keys=g.znaki_keys)


@app.route('/services/')
def services():
	return render_template('services.html', services=all_services,
											categories=g.all_categories)


@app.route('/service-item/<service_item_id>')
def service_item(service_item_id):
	service_item = Service.query.get(str(service_item_id))
	return render_template('service-item.html', service=service_item,
											categories=g.all_categories)


@login_required
@app.route('/file/')
def file():
	if not current_user.is_authenticated:
		return render_template('index.html', categories=g.all_categories, services=all_services)
	return render_template('file.html', categories=g.all_categories)


@app.route('/order', methods=['POST'])
def order():
	if request.method == 'POST':
		data = request.get_json()
		msg = Message(subject="Заказ товара с сайта 9004010.ru",
						sender="no-reply@jokerinteractive.ru",
						recipients=["origami@jokerinteractive.ru", data['sendTo']],
						charset="utf-8")
		msg.body = "Поля: " + str(data)
		msg.html = '<div style="background-color: #fff; width: 500px;">'
		msg.html += '<p style="color: #fff; background-color: #f97c00; font-size: 24px; padding: 15px 0; text-align: center; margin: 0;">Заказ товара!</p>'
		msg.html += '<div style="padding: 20px 40px 20px 80px;">'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Товар: <strong>' + data['good'] + '</strong></p>'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Телефон клиента: <strong><a href="tel: "' + data['tel'] + '" style="color: #2fa4e7; text-decoration: none;">' + data['tel'] + '</a></strong></p>'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Email клиента: <strong><a href="email: "' + data['mail'] + '" style="color: #2fa4e7; text-decoration: none;">' + data['mail'] + '</a></strong></p>'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Комментарии к заказу:' + data['comment'] + '</p>'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Время отправки: ' + datetime.datetime.now().ctime() + '</p>'
		msg.html += '<hr>'
		msg.html += '<p slyle="color: #000; font-size: 12px;">Заявка отправлена с сайта <a href="http://9004010.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">9004010.ru</a></p>'
		msg.html += '<p slyle="color: #000; font-size: 12px;">Сайт с любовью сделан студией <a href="https://jokerinteractive.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">jokerinteractive.ru</a></p>'
		msg.html += '</div>'
		msg.html += '</div>'
		mail.send(msg)
		return 'OK'


@app.route('/order-call', methods=['POST'])
def orderCall():
	if request.method == 'POST':
		data = request.get_json()
		msg = Message(subject="Заказ звонка с сайта 9004010.ru",
						sender="no-reply@jokerinteractive.ru",
						recipients=["origami@jokerinteractive.ru", data['sendTo']],
						charset="utf-8")
		msg.body = "Поля: " + str(data)
		msg.html = '<div style="background-color: #fff; width: 500px;">'
		msg.html += '<p style="color: #fff; background-color: #f97c00; font-size: 24px; padding: 15px 0; text-align: center; margin: 0;">Заказ обратного звонка!</p>'
		msg.html += '<div style="padding: 20px 40px 20px 80px;">'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Телефон клиента: <strong><a href="tel: "' + data['tel'] + '" style="color: #2fa4e7; text-decoration: none;">' + data['tel'] + '</a></strong></p>'
		msg.html += '<p slyle="color: #000; font-size: 18px;">Время отправки: ' + datetime.datetime.now().ctime() + '</p>'
		msg.html += '<hr>'
		msg.html += '<p slyle="color: #000; font-size: 12px;">Заявка отправлена с сайта <a href="http://antipark.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">antipark.ru</a></p>'
		msg.html += '<p slyle="color: #000; font-size: 12px;">Сайт с любовью сделан студией <a href="https://jokerinteractive.ru/" target="_blank" style="color: #2fa4e7; text-decoration: none;">jokerinteractive.ru</a></p>'
		msg.html += '</div>'
		msg.html += '</div>'
		mail.send(msg)
		return 'OK'


@login_required
@app.route('/update_market/')
def update_market():
    if not current_user.is_authenticated:
        return 'Not logged in'

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
                    pr = '1500'
                prods[col].append(pr)
            else:
                prods[col].append(getattr(product, col))

    df = pd.DataFrame(prods)
    df.set_index('id', inplace=True)
    df['local_delivery_cost'] = 1200
    df.rename(columns={'title': 'name'}, inplace=True)
    df.to_excel('database/market.xlsx')

    return 'OK'


@login_required
@app.route('/update_market_yml/')
def update_market_yml():
    if not current_user.is_authenticated:
        return 'Not logged in'

    import time
    now = time.strftime('%Y-%m-%d %H:%M', time.gmtime(time.time()))

    pricelist_xml = render_template('pricelist.yml', goods=all_goods, categories=all_categories,
                                                     now=now)
    response = make_response(pricelist_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@login_required
@app.route('/save_db/', methods=['POST'])
def save_db():
	if not current_user.is_authenticated:
		return 'Not logged in'

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


@login_required
@app.route('/get_db/')
def get_db():
	if not current_user.is_authenticated:
		return 'Not logged in'

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
