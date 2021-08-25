import functools, json

from flask import Blueprint, flash, g, redirect, render_template, \
    request, session, url_for, jsonify, current_app

from .models import *

import logging

from difflib import SequenceMatcher

#from .ReAI.ReAI import ReAI

# LOG : current_app.logger.warning()

bp = Blueprint("jasosul", __name__, url_prefix = '/jasosul')
# C:\\Users\\saeji\\Desktop\\My_Data\\1.Github_repositories\\JasoseoAI_project\\5.web\\re-ai\\flaskr\\Company\\CompanyInfo.json

with open('C:\\Users\\msi\\GitHub\\JasoseoAI_project\\5.web\\re-ai\\flaskr\\Company\\CompanyInfo.json', 'r', encoding='utf-8') as f:
    CompanyInfos = json.load(f)

#we = ReAI(generateNum=5)

@bp.route("/jasoList", methods = ['GET'])
def jasoList():
    # [1] username 가져오기 + user_id 가져오기
    username = session.get('username')
    user_id = userCheck(username)
    if not user_id:
        return redirect(url_for('index'))
    user_id = userCheck(username)['id']
    
    # [2] 해당 user인 cluster 가져오기
    jaso_lists = jasoListGet(user_id)
    #jaso_lists=['대한통운_1','삼성_1','lg_1']
    #current_app.logger.warning(jaso_lists)
    return render_template("jasosulList.html", username = username, jasosuls=jaso_lists)

# result 부분
@bp.route("/jasoContent", methods = ['GET'])
def jasoContent():
    # [1] get 가져오기
    username = request.args.get('username')
    ClusterId = request.args.get('ClusterId')
    title = request.args.get('title')

    user_id = userCheck(username)['id']
    current_app.logger.warning(username + " "+str(ClusterId) + title)

    # [2] 내용 가져오기
    allContents = jasoContentsLoad(user_id, ClusterId)

    # current_app.logger.warning(str(allContents[0]['idx']) + " " + \
    #     str(allContents[0]['Contentid']) + " " + \
    #         allContents[0]['question'] + " " +\
    #             allContents[0]['content'] + " ")

    return render_template("jasoResult.html", \
        username = username, ClusterId=ClusterId, title=title, \
            allContents = allContents)

@bp.route("/writeSetting", methods = ['GET'])
def writeSetting():
    username = session.get('username')

    return render_template("writeSetting.html", username = username)

@bp.route("/CompanySearch", methods = ['POST'])
def CompanySearch():
    username = session.get('username')
    CompanyNames = list(CompanyInfos.keys())
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

        # current_app.logger.warning(company)
        # current_app.logger.warning(title)

        cluster_id = jasoClusterCreate(user_id, title, company)

        current_app.logger.warning(cluster_id)

        CompanyInfo = {
            'Name' : company,
            'ImageQ' : CompanyInfos[company][0],
            'Cvalue' : CompanyInfos[company][1]
        }
        
    return render_template("jasoWrite.html", username=username, \
        ClusterId = cluster_id, \
        CompanyInfo=CompanyInfo,
        title = title)


@bp.route("/jasoRecommend", methods = ['POST'])
def jasoRecommend():
    recommendResults = []

    if request.method == 'POST':
        data = request.get_json()
        recommendText = data['recommendText']

        current_app.logger.warning(recommendText)

        #recommendResults = we.run_RecommendModel(recommendText)

        recommendResults = ['또한 교내 어학연수 프로그램을 통해 영어회화에 대한 자신감을, 토익을 통한 영어 관련 업무의 적응에도 어려움없이 해낼 거라 생각합니다.',\
            '쉽게 적응하리라 생각합니다. 아르바이트가 나태하고 힘들었던 저는 도망가고 싶었습니다',
            '쉽게 적응하리라 생각합니다. 아르바이트가 나태하고 힘들었던 저는 도망가고 싶었습니다',
            '쉽게 적응하리라 생각합니다. 아르바이트가 나태하고 힘들었던 저는 도망가고 싶었습니다',
            '쉽게 적응하리라 생각합니다. 아르바이트가 나태하고 힘들었던 저는 도망가고 싶었습니다']

    return jsonify(recommendResults = recommendResults)

@bp.route("/jasoAwkFind", methods = ['POST'])
def jasoAwkFind():
    awkResults = []

    if request.method == 'POST':
        data = request.get_json()
        AwkContent = data['AwkContent']

        current_app.logger.warning('##############################################')
        current_app.logger.warning(AwkContent)

        #strong, weak = we.run_ClassifierModel(AwkContent)

        strong = [(55, 80), (120, 160)]
        weak = [(30, 40)]
        
        total = []
        for st in strong: # strong = 1, weak = 2
            total.append([1, st[0], st[1]])
        for wk in weak:
            total.append([2, wk[0], wk[1]])
        total = sorted(total, key=lambda x: x[1])

        for i in range(len(total)):
            check, start, end = total[i]
            if i == 0:
                awkResults.append([0, AwkContent[:start]])
                
            else:
                awkResults.append([0, AwkContent[total[i-1][2]:start]])
            awkResults.append([check, AwkContent[start:end]])
        
        if total[-1][2] <= len(AwkContent)-1:
            awkResults.append([0, AwkContent[total[-1][2]:]])

        # for c in awkResults:
        #     current_app.logger.warning(c[1]+"$$$$$$$$$$$$")


    return jsonify(awkResults = awkResults)

@bp.route("/jasoWrite", methods = ['POST'])
def jasoWrite():
    if request.method == 'POST':
        data = request.get_json()
        username = session.get('username')
        user_id = userCheck(username)['id']

        ClusterId = data['ClusterId']
        Question = data['question']
        Content = data['content']

        if not username or not ClusterId or not Question or not Content:
            return jsonify(status = False)
        user_id = userCheck(username)['id']
        if not user_id:
            return jsonify(status = False)

        current_app.logger.warning("##############" +str(ClusterId))

        result = jasoSave(user_id, ClusterId, Question, Content)
        if not result:
            return jsonify(status = False)

    return jsonify(status = False) 