from flask import Flask, request as req, jsonify as json_res
from flask_cors import CORS,cross_origin
from db import db
app = Flask(__name__)
cors = CORS(app)
cursor = db.cursor()

@app.route("/login",methods=['POST'])
@cross_origin(origins=[u"*"])
def login():
    user = req.json
    cursor.execute('select * from users where username = "%s"'%user['username'])
    rows = cursor.fetchall()
    if len(rows)<=0:
        return json_res({'err':"Not found"}),404
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns,row)) for row in rows]
    res = data[0]
    if res['password']==user['password']:
        return json_res({"user":res,"token":{'type':res['role'],'id':res['u_id']}})
    else:
        return json_res({'err':"password not matched"}),401
        
@app.route("/task",methods=['GET'])
@cross_origin(origins=[u"*"])
def get_tasks():
    token = req.headers.get("authorization")
    print(type(token))
    return ""
    if token['type']=='admin':
        cursor.execute("select * from tasks")
        cols = [c[0] for x in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(cols,row)) for row in rows]
        return json_res(data)
    if token['type']=='user':
        cursor.execute('select * from tasks where createdBy = %d'%int(token['id']))
        cols = [c[0] for x in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(cols,row)) for row in rows]
        return json_res(data)

if __name__ == '__main__':
    app.run(debug=True)


