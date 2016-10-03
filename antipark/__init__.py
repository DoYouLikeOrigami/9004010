# -*- coding: utf-8 -*-
__author__ = 'JokerInteractive'
__email__ = 'info@jokerinteractive.ru'

import random
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result[:9]
    except:
        return seq

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['shuffle'] = filter_shuffle

db = SQLAlchemy(app)

mail = Mail(app)

from . import views
