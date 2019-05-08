# coding: utf-8
from flask import g


def login_log():
    print("login_log() ：current login user is " + g.user_name + " & login at " + str(g.user_login_time) + " & user ip:" + g.user_ip)
