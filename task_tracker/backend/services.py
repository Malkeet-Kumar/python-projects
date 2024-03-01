import jwt
from db import db
from flask import jsonify as json_res

secret = "this is what it is"

cursor = db.cursor()

def get_data(auth):
    try:
        if auth['type']=='admin':
            cursor.execute("select t.*, u.name, u.u_id from tasks t left join users u on t.createdBy=u.u_id")
            cols = [c[0] for c in cursor.description]
            print(cols)
            rows = cursor.fetchall()
            data = [dict(zip(cols,row)) for row in rows]
            print(data)
            return data
    
        if auth['type']=='user':
            cursor.execute('select * from tasks where createdBy = %s'%auth['id'])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(cols,row)) for row in rows]
            return data
        
    except Exception as e:
        return e
    
def get_user(user):
    try:
        print(user)
        cursor.execute('select * from users where username = "%s"'%user['username'])
        rows = cursor.fetchall()
        if len(rows)<=0:
            return {'err':"Not found"},404
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns,row)) for row in rows]
        res = data[0]
        if res['password']==user['password']:
            token = jwt.encode({'type':res['role'],'id':res['u_id']},secret,algorithm='HS256',headers={"alg": "HS256","typ": "JWT"})
            return {"user":res,"token":token},200
        else:
            return {'err':"password not matched"},401
    except Exception as e:
        return repr(e),500
    

def create_user(user):
    try:
        val = tuple([x for x in user.values()])
        print("insert into users values('',%s,%s,%s,'user')",val)
        cursor.execute("insert into users values('',%s,%s,%s,'user')",val)
        db.commit()
        if cursor.rowcount>0:
            return {"msg":"success"},200
        else:
            return {"err":'error occured while inserting'},304
    except Exception as e:
        return {"err":repr(e)},500
    
def create_task(task,id):
    try:
        val = tuple([x for x in task.values()]+[id])
        cursor.execute("insert into tasks values('',%s,%s,%s,%s,0,%s,%s)",val)
        db.commit()
        cursor.execute('select * from tasks order by task_id desc limit 1')
        cols = [c[0] for c in cursor.description]
        task = dict(zip(cols,cursor.fetchone()))
        task['u_id'] = id
        print(task)
        if cursor.rowcount>0:
            return {'msg':'success', 'task':task},200
        else:
            return {'err':'error while insertig'},304
    except Exception as e:
        return {"err": repr(e)},500
    
def delete_task(task_id,auth):
    try:
        if auth['type']=='admin':
            cursor.execute('delete from tasks where task_id = "%s"'%task_id)
            print(cursor.rowcount)
    except Exception as e:
        return {'err':repr(e)},500
    
def update_status(task_id, status,auth):
    try:
        if auth['type']=='admin':
            print("admin->")
            print("update tasks set status = %s"%status+' where task_id = "%s"'%task_id)
            cursor.execute("update tasks set status = %s"%status+' where task_id = "%s"'%task_id)
            print(cursor.rowcount)
            if cursor.rowcount>0:
                return {"msg":"success"},200
            else:
                return {'err':'error while updating maybe record does not exists'}
        else:
            cursor.execute("update tasks set status = %s"%status+' where task_id = "%s"'%task_id+' and createdBy = "%s"'%auth['id'])
            print(cursor.rowcount)
            if cursor.rowcount>0:
                return {"msg":"success"},200
            else:
                return {'err':'error while updating maybe record does not exists'}
    except Exception as e:
        return {"err":repr(e)},500