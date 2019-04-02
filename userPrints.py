import datetime

def getUserPrints(db, cursor, sessionId, type):

    fd = open('scripts/get/user/prints.sql', 'r')
    sql = fd.read() % (sessionId, type)
    fd.close()
    cursor.execute(sql)
    
    result = cursor.fetchall()
    prints = []

    # TODO: Move into a datapreparer Function
    # Ignre row8,9 because id, userid not necessary

    for row in result:
        data = {
            "id": row[0],
            "filename": row[1],
            "name": row[2],
            "time": row[3],
            "timeReal": row[4],
            "length": row[5],
            "weight": row[6],
            "price": row[7],
            "spoolId": row[10],
            "amount": row[11],
            "date": row[13].strftime('%Y-%m-%d'),
            "date_until": row[14].strftime('%Y-%m-%d'),
            "date_done": row[15].strftime('%Y-%m-%d'),
            "notes": row[16]
        }
        
        prints.append(data)
    print(prints)
    return prints