import bcrypt
# https://pypi.org/project/bcrypt/


def login(db, cursor, info):
    # Important: When using bcrypt functions: string has to be .encode('utf-8')

    sql = "SELECT password FROM user WHERE email = '%s'" % (info["email"])
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result[0][0].encode('utf-8'))

    if compare(info["password"], result[0][0]):
        sql  = "SELECT sessionId FROM user WHERE email = '%s'" % (info["email"])
        cursor.execute(sql)
        result = cursor.fetchall()
        
        return result[0][0]
    else:
        return "Error"

def register(db, cursor, info):
    fd = open('scripts/post/user.sql', 'r')
    sql = fd.read()
    fd.close()

    sessionId = genSessionId(info["username"], info["password"])
    
    val = (info["username"], info["email"], encrypt(info["password"]), sessionId)
    
    cursor.execute(sql, val)

    db.commit()
    
    return sessionId

def changePassword():
    return ""


# ----- Bcrypt Functions -----
def compare(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def encrypt(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def genSessionId(username, password):
    # TODO: Create real session ID
    return "928374" + password