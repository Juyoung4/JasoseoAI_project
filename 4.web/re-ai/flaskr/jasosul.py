import functools

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *

import logging

bp = Blueprint("jasosul", __name__, url_prefix = '/jasosul')

@app.route("/jasoList", methods = 'GET')
def jasoList():

    return render_template("boardList.html")