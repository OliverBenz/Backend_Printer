def newPrint(db, cursor, obj):
    # Print
    fd = open('scripts/post/print.sql', 'r')
    sql = fd.read()
    fd.close()

    val = (obj["filename"], obj["name"], obj["time"], 0.00, obj["length"], obj["weight"], obj["price"])
    
    cursor.execute(sql, val)

    # History
    fd = open('scripts/post/history.sql', 'r')
    sql = fd.read()
    fd.close()

    val = (obj["usrid"], obj["amount"], obj["date"], obj["date_until"], "9999-01-01", int(cursor.lastrowid))
    
    # TODO: More beautiful solution
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    cursor.execute(sql, val)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    
    db.commit()

    return ""