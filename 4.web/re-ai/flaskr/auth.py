import functools

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *
from .form import *
from flask_wtf.csrf import CSRFProtect

import logging

bp = Blueprint("auth", __name__, url_prefix = '/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    # 회원가입 시 받을 목록 : username, password
    form = RegisterForm()
    error = None

    if form.validate_on_submit(): # 내용이 채워져 있는지 아닌지 까지 체크해줌
        username = form.data.get("username")
        passwd = form.data.get("passwd")

        if registers(username, passwd):
            # session 추가
            session.clear()
            session['username'] = username
            return redirect(url_for("auth.login"))
        else:
            error = 'User {} is already registered'.format(username)
    
        if error != None:
            logging.debug("error!!! : ", error)
            flash(error)

    return render_template('auth/register.html', form=form)

@bp.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data.get('username')
        passwd = form.data.get('passwd')

        if logins(username, passwd):
            return redirect(url_for("main.main"))
        else:
            flash("passwod Incorrect")

    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            "select * FROM users WHERE username = ?", (username, )
        ).fetchone()

@bp.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for("main.main"))