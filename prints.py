def get(db, cursor):
    sql = "SELECT * FROM prints"
    cursor.execute(sql)
    result = cursor.fetchall()
    prints = []
    for row in result:
        data = {
            'id': row[0],
            'filename': row[1],
            'name': row[2],
            'time': row[3],
            'length': row[4],
            'weight': row[5],
            'price': row[6],
            'time_real': row[7]
        }
        prints.append(data)

    return prints

def post(db, cursor, value):
    # TODO: SQL Statement
    return ""