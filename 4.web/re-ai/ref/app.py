from datetime import datetime
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='HOME PAGE')

@app.route('/board', methods = ['GET', 'POST'])
def board():
    if request.method=='POST':
        title=request.form["title"]
        company=request.form.get("company")
        print(company)
    return render_template('board.html', title=title, company=company)

@app.route('/boardList')
def boardList():
    posts=['대한통운_1','삼성_1','lg_1']
    return render_template('boardList.html', posts=posts)

@app.route('/writeSetting', methods = ['GET', 'POST'])
def writeSetting():
    return render_template('writeSetting.html')

@app.route('/ackward', methods = ['GET', 'POST'])
def ackward():
    if request.method == 'POST':
         data = request.get_json()
         acksent = data['sentence']
         state = data['state']
         if not acksent or not state:
            return jsonify(state_check = "Value Error!", result = dict())
    return jsonify(state_check = "success", result= data)

@app.route('/keywords')
def keywords():
    # 키워드 뽑아서 만들고

    # 보여줄게
    # [1] 내가 쓴 모든 질문과 내용들

    # [2] 회사 키워드들 

    return render_template('result.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST': # 질문, 내용 받아옴

        data = request.get_json()
        question = data['question']
        content = data['content']
        state = data['state']
        if not question or not content or not state:
            return jsonify(state_check = "Value Error!", result = dict())
        
        print(data)
        # 만약에 계속 한다는 의미이면 내용 저장해두고, 기달리기

        # 내용 처리 => MODEL에 전달함
        # [2] 첫번째 모델에 전달
        #result1 = questions
        # [3] 두번째 모델에 전달
    return jsonify(state_check = "success", result= data)

    
if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)