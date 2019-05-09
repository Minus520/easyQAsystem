# coding: utf-8
from flask import Blueprint

my_error = Blueprint('error', __name__)

from . import error
