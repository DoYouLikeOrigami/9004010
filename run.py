#!.venv/bin/python
__author__ = 'Joker Interactive'
__email__ = 'info@jokerinteractive.ru'
import os

#from config import UPLOAD_PATH
from antipark import app as application

if __name__ == '__main__':

    # Create upload directory
    #try:
    #    os.mkdir(UPLOAD_PATH)
    #except OSError:
    #    pass
    application.run(host='0', port=4444)
