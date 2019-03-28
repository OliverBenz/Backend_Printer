import bcrypt
# https://pypi.org/project/bcrypt/

# Bcrypt Functions
def compare(password, hash):
    return bcrypt.checkpw(password, hash)

def encrypt(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def genSessionId(username, password):
    # TODO: Create real session ID
    return encrypt(username + password)

def newUser(db, cursor, username, password):
    fd = open('scripts/post/user.sql', 'r')
    sql = fd.read()
    fd.close()
    
    val = (username, encrypt(password), genSessionId(username, password))
    
    cursor.execute(sql, val)
    db.commit()
    
    return ""

def login(db, cursor, info):
    username, password = info.split("-")
    print(username, password)
    # 1) Get username/password
    # 2) Compare password with hash
    # 3) If right -> Get sessionId
    # 4) Return sessionId
    return ""