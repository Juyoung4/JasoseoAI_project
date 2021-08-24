from datetime import datetime
from . import db

def query_db(query, args=(), one=False):
    cur = db.get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    cur = db.get_db().execute(query, args)
    db.get_db().commit() # insert는 commit() 꼭!
    return cur.lastrowid

def registers(username, passwd = None):
    if query_db("SELECT id FROM users WHERE username = ?", [username], one=True) is None: # 중복 검사
        return False
    else:
        return insert_db("INSERT INTO users (username, passwd) values (?, ?)", [username, passwd])

def logins(username, passwd):
    cur = query_db("SELECT id FROM users WHERE username = ?", [username], one=True)
    
    if cur is not None:
        return query_db("SELECT id FROM users WHERE username = ? and passwd = ?", [username, passwd], one=True)
    else:
        return False

def userCheck(username):
    return query_db("SELECT id FROM users WHERE username = ?", [username], one=True)

def jasoListGet(userId):
    jasoLists = []

    for jaso in query_db("SELECT title, company, create_at FROM clusters WHERE writer_id = ? ORDER BY create_at", [userId]):
        jasoLists.append({
            'title' : jaso['title'],
            'company' : jaso['company'],
            'create_at' : jaso['create_at']
        })

    return jasoLists if jasoLists else None


def jasoClusterCreate(userId, title, create_at):
    return insert_db("INSERT INTO clusters (writer_id, title, company) values (?, ?, ?)", \
        [userId, title, create_at])