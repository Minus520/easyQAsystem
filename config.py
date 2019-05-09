# coding: utf-8
import os

DEBUG = True
SECRET_KEY = 'smtp.cntaiping.com'  # os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xroot@10.1.14.230:3306/easyQAsystem?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAIL_SERVER = 'smtp.cntaiping.com'
MAIL_PORT = 25
# MAIL_USE_TLS = True
MAIL_USERNAME = 'yaoxing@fsc.cntaiping.com'
MAIL_PASSWORD = 'Abc12345'
