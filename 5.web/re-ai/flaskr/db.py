import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g: # g는 재사용함 (처음에만 g 설정)
        g.db = sqlite3.connect(
            # current_app => request를 발생시킨 flask 앱
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False,
        )

        # sqlite3.Row => 쿼리를 실행했을 때 결과를 딕셔너리 형태로 돌려준다
        # 
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# get_db를 통해 DB Connection을 맺는다.
# create 등 schema와 관련된 명령어
def init_db():
    db = get_db()
    
    # open_resource()를 통해 상대 위치에서 지정한 파일 'schema.sql'파일을 가져온다
    with current_app.open_resource('schema.sql') as f:
        # 그리고 f.read()를 통해 파일을 읽어오라는 명령 실행
        db.executescript(f.read().decode('utf-8'))

    current_app.logger.info("Database initialize done.")

# get_db를 통해 DB Connection을 맺는다.
# table - insert, delete 등 과 관련된 명령어 실행
def load_fixture():
    db = get_db()
    
    with current_app.open_resource("data.sql") as f:
        db.executescript(f.read().decode("utf8"))

    current_app.logger.info("Fixture load done.")

@click.command("init-db") # 이 명령어를 통해 db를 초기화함
@with_appcontext
def init_db_command(): # 새로운 테이블 생성 및 기존 데잍 삭제
    """Clear the existing data and create new tables."""
    init_db()
    load_fixture()
    click.echo("Initialized the database.")

# close_db와 init_db_command을 앱 인스턴스로 등록해야 앱에서 사용 가능
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)