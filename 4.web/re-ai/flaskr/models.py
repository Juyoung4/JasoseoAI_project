from datetime import datetime
from . import db

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    cur = db.get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db.get_db().execute(query, args)
    db.get_db().commit()
    return True

def registers(username, passwd = None):
    if query_db("select id FROM users WHERE username = ?", [username], one=True) is None: # 중복 검사
        return False
    else:
        db.get_db().execute("insert into users (username, passwd) values (?, ?)", (username, passwd, ))
        db.get_db().commit() # insert는 commit() 꼭!
        return True

def logins(username, passwd):
    cur = query_db("select id FROM users WHERE username = ?", [username], one=True)
    
    if cur is not None:
        return query_db("select id FROM users WHERE username = ?", [username, passwd], one=True)
    else:
        return False

def userCheck(username):
    return query_db("select id FROM users WHERE username = ?", [username], one=True)

def jasoListGet(userId):
    return