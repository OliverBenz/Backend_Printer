import bcrypt
# https://pypi.org/project/bcrypt/

# ----- Main Functions -----
def login(db, cursor, info):
    sql = "SELECT password FROM user WHERE email = '%s'" % (info["email"])
    cursor.execute(sql)
    result = cursor.fetchall()

    if compare(info["password"], result[0][0]):
        sql  = "SELECT sessionId FROM user WHERE email = '%s'" % (info["email"])
        cursor.execute(sql)
        result = cursor.fetchall()
        
        return result[0][0], True, 200
    else:
        return "Error", False, 400


def register(db, cursor, info):
    fd = open('scripts/post/user.sql', 'r')
    sql = fd.read()
    fd.close()

    sessionId = genSessionId(info["username"], info["password"])
    val = (info["username"], info["email"], encrypt(info["password"]), sessionId)
    
    cursor.execute(sql, val)
    db.commit()
    
    if cursor.rowcount == 0:
        return "Error", False, 400
    else:
        return sessionId, True, 200


def changePW(db, cursor, info):
    # TODO: Add changePW function

    return "Function not yet implemented", False, 400


def checkLoggedIn(cursor, sessionId):
    status = False

    sql = "SELECT count(id) FROM user WHERE sessionId = '%s'" % (sessionId)
    cursor.execute(sql)
    result = cursor.fetchall()

    if result[0][0] == 1:
        status = True
    
    return status


# ----- Helper Functions -----
def genSessionId(username, password):
    username = encrypt(username)
    password = encrypt(password)

    sessionId = username[0:round(len(username) / 2)].lower() + password[round(len(password) / 2):].upper()

    # TODO: Create real session ID
    return str(sessionId).replace("/", "-").replace("'", "")


# ----- Bcrypt Functions -----
def compare(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def encrypt(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

