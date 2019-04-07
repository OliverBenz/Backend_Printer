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
        sessionId = cursor.fetchall()[0][0]

        if checkUserGroup(cursor, sessionId) != "Registered":
            return sessionId, True, 200
        else:
            return "User not verified", False, 403
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
        return "Successful", True, 200


def changePW(db, cursor, info):
    sql = "SELECT password FROM user WHERE sessionId = '%s'" % info["sessionId"]
    cursor.execute(sql)

    if compare(info["passwordOld"], cursor.fetchall()[0][0]):
        sessionId = genSessionId(info["passwordOld"], info["passwordNew"])

        fd = open('scripts/post/userChangePw.sql', 'r')
        sql = fd.read() % (encrypt(info["passwordNew"]), sessionId, info["sessionId"])
        fd.close()

        cursor.execute(sql)
        db.commit()

        if cursor.rowcount == 0:
            return "Could not change password", False, 500
        else:
            return sessionId, True, 200

    else:
        return "Wrong password", False, 401

    # TODO: Add changePW function
    # Get user password with sessionId
    # Check if password is correct
    # Update password to new
    # Update sessionId to new
    # Return new sessionId

    return "Function not yet implemented", False, 400


def getGroup(db, cursor, sessionId):
    return checkUserGroup(cursor, sessionId), True, 200


# ----- Helper Functions -----
def checkLoggedIn(cursor, sessionId):
    status = False

    sql = "SELECT count(id) FROM user WHERE sessionId = '%s'" % (sessionId)
    cursor.execute(sql)
    result = cursor.fetchall()

    if result[0][0] == 1:
        status = True

    return status


def checkUserGroup(cursor, sessionId):
    fd = open('scripts/get/userGroup.sql', 'r')
    sql = fd.read() % sessionId
    fd.close()

    cursor.execute(sql)

    return cursor.fetchall()[0][0]


def genSessionId(username, password):
    username = encrypt(username)
    password = encrypt(password)

    sessionId = username[0:round(len(username) / 2)].lower() + password[round(len(password) / 2):].upper()

    # TODO: Create real session ID
    return str(sessionId).replace("/", "-").replace("b'", "").replace("'", "")


# ----- Bcrypt Functions -----
def compare(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


def encrypt(password):
    return str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).replace("b'", "").replace("'", "")

