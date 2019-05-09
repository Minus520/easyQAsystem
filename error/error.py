# coding: utf-8
from flask import render_template
from . import my_error


@my_error.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@my_error.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
