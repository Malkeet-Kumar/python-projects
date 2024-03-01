from flask import Flask, request as req, jsonify as json_res
from flask_cors import CORS,cross_origin
import jwt
from services import get_data, get_user, create_user, secret, create_task, delete_task,update_status

app = Flask(__name__)
cors = CORS(app)

@app.route("/login",methods=['POST'])
@cross_origin(origins=[u"*"])
def login():
    user = req.json
    return get_user(user)

@app.route("/signup",methods=['POST'])
@cross_origin(origins=[u"*"])
def signup():
    return create_user(req.json)
        
@app.route("/task",methods=['GET','POST','PUT','PATCH','DELETE'])
@cross_origin(origins=[u"*"])
def task_ops():

    token = req.headers.get("authorization")
    if token==None or token=="":
        return json_res({"err":"unauthorised access"}),401
    
    auth = jwt.decode(token, secret, algorithms=['HS256']) 

    match req.method:
        case 'GET':
            return json_res(get_data(auth))
        
        case 'POST':
            return json_res(create_task(req.json, auth['id']))
        
        case "DELETE":
            return json_res(delete_task(req.args.get('id'), auth))
        
        case "PATCH":
            return json_res(update_status(req.args.get('id'), req.args.get('status'), auth))
        
        
if __name__ == '__main__':
    app.run(debug=True)


