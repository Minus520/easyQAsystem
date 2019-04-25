# coding: utf-8
from flask import g


def login_log():
    print(g.user_name)
