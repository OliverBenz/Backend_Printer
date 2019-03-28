def formatName(filename):
    # Filename:     usrid-amount-date-date_till-filename-name-time-length-weight-price
    
    new = filename.split("-")

    # Time_Real added later
    obj = {
        "usr": new[0],
        "amount": new[1],
        "date": new[2].replace(".", "-"),
        "date_till": new[3].replace(".", "-"),
        "filename": new[4],
        "name": new[5],
        "time": float(new[6]),
        "length": float(new[7]),
        "weight": float(new[8]),
        "price": float(new[9]),
        "time_real": 0.00
    }
    return obj 

def addPrint(db, cursor, obj):
    # Read script
    fd = open('scripts/post/print.sql', 'r')
    sql = fd.read()
    fd.close()

    # Gen Value
    val = (obj["filename"], obj["name"], obj["time"], obj["length"], obj["weight"], obj["price"], obj["time_real"])

    # Execute Script
    cursor.execute(sql, val)
    db.commit()

    return ""

def addHistory(db, cursor, obj):
    # Read script
    fd = open('scripts/post/history.sql', 'r')
    sql = fd.read()
    fd.close()
    print(sql)
    # Gen Value
    val = (obj["usr"], obj["amount"], obj["date"], obj["date_till"], 0, 0, obj["filename"])

    cursor.execute(sql, val)
    db.commit()

    return ""

def newPrint(db, cursor, filename):
    obj = formatName(filename)
    addPrint(db, cursor, obj)
    addHistory(db, cursor, obj)