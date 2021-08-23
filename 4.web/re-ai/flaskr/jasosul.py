import functools, json

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *

import logging

# LOG : current_app.logger.warning()

bp = Blueprint("jasosul", __name__, url_prefix = '/jasosul')

@bp.route("/jasoList", methods = ['GET'])
def jasoList():
    # [1] username 가져오기 + user_id 가져오기
    username = session.get('username')
    user_id = userCheck(username)['id']
    
    # [2] 해당 user인 cluster 가져오기
    jaso_lists = jasoListGet(user_id)
    #jaso_lists=['대한통운_1','삼성_1','lg_1']
    #current_app.logger.warning(jaso_lists)
    return render_template("jasosulList.html", jasosuls=jaso_lists, username = username)

@bp.route("/jasoContent", method = ['GET'])
def jasoContent():
    
    return render_template()