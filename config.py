# coding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xroot@10.1.14.230:3306/easyQAsystem?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
