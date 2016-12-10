# -*- coding: utf-8 -*-
__author__ = 'JokerInteractive'
__email__ = 'info@jokerinteractive.ru'

import re
import random
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result[:9]
    except:
        return seq

def str_to_dict(str):
    return eval(str).items()

def only_digits(str):
    return re.sub('\D', '', str)

def other_if_none(str):
    return str if str else 'Прочее'

# def format_datetime(value):
#     format="EEEE-MM-dd y  HH:mm"
#     elif format == 'medium':
#         format="EE dd.MM.y HH:mm"
#     return babel.dates.format_datetime(value, format)
#
# jinja_env.filters['datetime'] = format_datetime

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['shuffle'] = filter_shuffle
app.jinja_env.filters['str_to_dict'] = str_to_dict
app.jinja_env.filters['digits'] = only_digits
app.jinja_env.filters['other_if_none'] = other_if_none

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

mail = Mail(app)

from . import views
