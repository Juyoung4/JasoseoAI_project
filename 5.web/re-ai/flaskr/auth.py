import functools

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *

import logging

bp = Blueprint("auth", __name__, url_prefix = '/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    # 회원가입 시 받을 목록 : username, password
    if request.method == 'POST':
        # template에서 받아오는거니까 form 형식
        username = request.form["username"]
        passwd = request.form["passwd"]

        error = "None"

        if not username:
            error = 'username is required'
        elif not passwd:
            error = 'passwd is required'
        else: # DB에 저장
            if registers(username=username, passwd=passwd):
                # session 추가
                session.clear()
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = 'User {} is already registered'.format(username)

        if error is not "None":
            flash(error)
            
    return render_template('register.html')

@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']

        if not username:
            error = 'username is required'
        elif not passwd:
            error = 'passwd is required'
        else: # DB 확인
            if logins(username, passwd):
                session.clear()
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = 'Incorrect password'
        flash(error)
    return render_template('login.html')


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
    return redirect(url_for("index"))