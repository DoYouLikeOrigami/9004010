#!/usr/bin/env python
__author__ = 'Joker Interactive'
__email__ = 'info@jokerinteractive.ru'

import subprocess, sys
from flask_script import Manager

from antipark import app, db


manager = Manager(app)


@manager.command
def createdb(drop_first=False):
    """Creates the database."""
    # if drop_first:
    # db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
