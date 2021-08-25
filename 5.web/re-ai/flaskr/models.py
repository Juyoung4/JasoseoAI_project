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
    if query_db("SELECT id FROM users WHERE username = ?", [username], one=True) != None: # 중복 검사
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

def CompanyLoad(ClusterId):
    return query_db("SELECT company FROM clusters WHERE id = ?", [ClusterId], one=True)

def jasoClusterCreate(userId, title, company):
    return insert_db("INSERT INTO clusters (writer_id, title, company) values (?, ?, ?)", \
        [userId, title, company])

def jasoListGet(userId):
    jasoLists = []

    for jaso in query_db("SELECT id, title, company, create_at FROM clusters WHERE writer_id = ? ORDER BY create_at", [userId]):
        jasoLists.append({
            'ClusterId' : jaso['id'],
            'title' : jaso['title'],
            'company' : jaso['company'],
            'create_at' : jaso['create_at']
        })

    return jasoLists if jasoLists else None

def jasoSave(userId, clusterId, question, content):
    return insert_db("INSERT INTO jasosuls (writer_id, cluster_id, question, content) values (?, ?, ?, ?)", \
        [userId, clusterId, question, content])

def jasoContentsLoad(userId, clusterId):
    jasoContents = []

    for idx, jaso in enumerate(query_db("SELECT id, question, content, create_at FROM jasosuls WHERE writer_id = ? AND cluster_id = ? ORDER BY create_at", [userId, clusterId])):
        
        jasoContents.append({
            'idx' : idx+1,
            'Contentid' : jaso['id'],
            'question' : jaso['question'],
            'content' : jaso['content'],
            'create_at' : jaso['create_at']
        })

    return jasoContents if jasoContents else None