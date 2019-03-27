def get(db, cursor):
    sql = "SELECT * FROM prints"
    cursor.execute(sql)
    result = cursor.fetchall()
    for a in result:
        print('id: ', a[0])
        print('filename: ', a[1])
    
    return result

def post(db, cursor, value):
    # TODO: SQL Statement
    return ""