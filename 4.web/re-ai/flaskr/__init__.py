import os

# flask 선언
from flask import Flask, session, render_template

# create_app => 어플리케이션 팩토리
def create_app(test_config=None):
    # application 생성 및 구성(Flask 인스턴스 생성)
    app = Flask(__name__, instance_relative_config=True)
        # app의 기본 설정 세팅
            # SECRET_KEY = 데이터 보안(지금은 개발이니까 'dev')
            # DATABASE = SQLite 데이터베이스 파일 경로
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'), # join(dirname(dirname(__file__)), "db.sqlite3"),
    )

    app.config["DEBUG"] = True
    if app.debug:
        print('running in debug mode')
    else:
        print('NOT running in debug mode')

    if test_config is None:
        # test x => 기존 instacne config 불러옴
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # instacne folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # DB 관련 등록
    from . import db
    db.init_app(app)

    # index페이지-home 등록
    @app.route("/")
    def index():
        username = session.get('username', None)
        return render_template('index.html', username = username)

    # Blueprint "auth" 등록
    from . import auth
    app.register_blueprint(auth.bp)

    # Blueprint "jasosul" 등록
    from . import jasosul
    app.register_blueprint(jasosul.bp)
    
    return app

