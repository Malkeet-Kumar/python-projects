from db import db
class User:
    cursor = db.cursor()
    def __init__(self, name, username, password, role, id):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.u_id = id

    def login(self ,user):
        try:
            User.cursor.execute('select * from users where username = "%s"'%user['username'])
            res = User.cursor.fetchone()
            if res!='None':
                return None
            else:
                return res
        except Exception as e:
            print("error",repr(e))
        
    def to_tuple(self):
        return (self.u_id, self.name, self.username, self.password, self.role)
    
    def signup(self):
        try:
            User.cursor.execute("insert into users values (%s,%s,%s,%s,%s)",self.to_tuple())
            db.commit()
            if User.cursor.rowcount>0:
                return 0
            return 1
        except Exception as e:
            print("Error->", repr(e))
            return -1

# if a<0:
#     print("error")
# elif a>0:
#     print("Somthing wrong")
# else:
#     print("Success")