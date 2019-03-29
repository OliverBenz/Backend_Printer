import bcrypt
# https://pypi.org/project/bcrypt/


def login(db, cursor, info):
    # Important: When using bcrypt functions: string has to be .encode('utf-8')

    sql = "SELECT password FROM user WHERE name = '%s'" % (info["username"])
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result[0][0].encode('utf-8'))

    if compare(info["password"], result[0][0]):
        sql  = "SELECT sessionId FROM user WHERE name = '%s'" % (info["username"])
        cursor.execute(sql)
        result = cursor.fetchall()

        return result[0][0]
    else:
        return "Wrong password"

def newUser(db, cursor, username, password):
    fd = open('scripts/post/user.sql', 'r')
    sql = fd.read()
    fd.close()
    
    val = (username, encrypt(password), genSessionId(username, password))
    
    cursor.execute(sql, val)
    db.commit()
    
    return ""

def changePassword():
    return ""


# ----- Bcrypt Functions -----
def compare(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def encrypt(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def genSessionId(username, password):
    # TODO: Create real session ID
    return encrypt(username + password)