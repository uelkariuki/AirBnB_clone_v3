#!/usr/bin/python3

from flask import Blueprint
from api.v1.views.index import *
""" Importing required modules"""

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
