def get(db, cursor):
    sql = "SELECT id, filename FROM prints"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return result

def post(db, cursor, value):
    # TODO: SQL Statement
    return ""