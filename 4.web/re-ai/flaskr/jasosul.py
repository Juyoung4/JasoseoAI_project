import functools, json

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *

import logging

from difflib import SequenceMatcher

# LOG : current_app.logger.warning()

bp = Blueprint("jasosul", __name__, url_prefix = '/jasosul')

with open('C:/Users/msi/GitHub/JasoseoAI_project/4.web/re-ai/flaskr/Company/CompanyInfo.json', 'r', encoding='utf-8') as f:
    CompanyInfo = json.load(f)

@bp.route("/jasoList", methods = ['GET'])
def jasoList():
    # [1] username 가져오기 + user_id 가져오기
    username = session.get('username')
    user_id = userCheck(username)['id']
    
    # [2] 해당 user인 cluster 가져오기
    jaso_lists = jasoListGet(user_id)
    #jaso_lists=['대한통운_1','삼성_1','lg_1']
    #current_app.logger.warning(jaso_lists)
    return render_template("jasosulList.html", username = username, jasosuls=jaso_lists)

# result 부분
@bp.route("/jasoContent", methods = ['GET'])
def jasoContent():

    return render_template()

@bp.route("/writeSetting", methods = ['GET'])
def writeSetting():
    username = session.get('username')

    return render_template("writeSetting.html", username = username)

@bp.route("/CompanySearch", methods = ['POST'])
def CompanySearch():
    username = session.get('username')
    CompanyNames = list(CompanyInfo.keys())
    Candidates = []
    
    if request.method == 'POST':
        data = request.get_json()
        CompanyName = data['searchCompany']
        if not CompanyName:
            return jsonify(Candidates = Candidates)

        # 유사도 검사
        for company in CompanyNames:
            if SequenceMatcher(None, CompanyName, company).ratio() >= 0.5:
                Candidates.append(company)
    return jsonify(Candidates = Candidates)

@bp.route("/ClusterCreate", methods = ['GET', 'POST'])
def ClusterCreate():
    if request.method == 'POST':
        # [1] 먼저 cluster 생성 - 필요 정보 => writer_id, title, company!
        username = session.get('username')
        user_id = userCheck(username)['id']

        title=request.form.get("jasoTitle")
        company=request.form.get("companyList")

        current_app.logger.warning(company)
        current_app.logger.warning(title)

        cluster_id = jasoClusterCreate(user_id, title, company)

        current_app.logger.warning(cluster_id)

    return render_template("jasoWrite.html", username=username, \
        ClusterId = cluster_id, \
        CompanyName=company)


