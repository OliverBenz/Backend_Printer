def get(db, cursor, value):
    value = value.replace("-", " ")
    
    fd = open('scripts/get/prints.sql', 'r')
    sql = fd.read() % value
    fd.close()

    cursor.execute(sql)
    result = cursor.fetchall()
    prints = []

    # TODO: Move into a datapreparer Function
    for row in result:
        data = {
            "id": row[0],
            "filename": row[1],
            "name": row[2],
            "time": row[3],
            "length": row[4],
            "weight": row[5],
            "price": row[6],
            "time_real": row[7]
        }
        prints.append(data)

    return prints

def post(db, cursor, value):
    # TODO: SQL Statement
    return ""