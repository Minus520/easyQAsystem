# coding: utf-8
from flask import Blueprint

my_main = Blueprint('main', __name__)

from . import main
