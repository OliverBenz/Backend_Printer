import user

def getPrint(db, cursor, status):
    if status == "to-do":
        status = "To Do"

    # User doesn't have to be logged in -> No Job information, just print
    fd = open('scripts/get/print.sql', 'r')
    sql = fd.read() % status
    fd.close()
    
    cursor.execute(sql)
    result = cursor.fetchall()
    prints = []
    
    for row in result:
        data = {
            "id": row[0],
            "filename": row[1],
            "name": row[2],
            "time": row[3],
            "length": row[4],
            "weight": row[5],
            "price": row[6]
        }
        prints.append(data)
    
    return prints, True, 200


def getJob(db, cursor, info):
    # ----- Check if user is logged in -----
    if user.checkLoggedIn(cursor, info["sessionId"]):
        if info["status"] == "to-do":
            info["status"] = "To Do"

        fd = open('scripts/get/job.sql', 'r')
        sql = fd.read() % (info["sessionId"], info["status"])
        fd.close()

        cursor.execute(sql)
        
        result = cursor.fetchall()
        prints = []

        # Ignore row8,9 because id, userid not necessary
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
                "dateUntil": "",
                "dateDone": "",
                "notes": row[16]
            }
            if row[14]:
                data["dateUntil"] = row[14].strftime('%Y-%m-%d')
            if row[15]:
                data["dateDone"] = row[15].strftime('%Y-%m-%d')
    
            prints.append(data)

        return prints, True, 200

    return "Not logged in", False, 403


def postJob(db, cursor, obj):
    # ----- Check if user is logged in -----
    if user.checkLoggedIn(cursor, obj["sessionId"]):
        
        # ----- Check if filename already exists -----
        sql = "SELECT count(id) from prints WHERE filename = '%s'" % obj["filename"]
        cursor.execute(sql)

        printId = 0
        # ----- If Filename exsts: getId - If not: insert -----
        if cursor.fetchall()[0][0] > 0:
            sql = "SELECT id from prints WHERE filename = '%s'" % obj["filename"]
            cursor.execute(sql)
            printId = cursor.fetchall()[0][0]
        else:
            # ----- Add Print -----
            fd = open('scripts/post/print.sql', 'r')
            sql = fd.read()
            fd.close()
            
            val = (obj["filename"], obj["name"], obj["time"], 0.00, obj["length"], obj["weight"], obj["price"])
            
            cursor.execute(sql, val)

            # ----- Catch failed add -----
            if cursor.rowcount == 0:
                return "Error print add", 409

            printId = int(cursor.lastrowid)


        # ----- Add Job -----
        fd = open('scripts/post/job.sql', 'r')
        sql = fd.read()
        fd.close()

        if obj["date_until"] == "0000-00-00":
            obj["date_until"] = "9999-01-01"

        # Not with cursor.lastrowid
        val = (obj["sessionId"], obj["amount"], obj["date"], obj["date_until"], "9999-01-01", obj["notes"], printId)

        # TODO: More beautiful solution
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(sql, val)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        db.commit()

        return "Successfully added Job", True, 200
    return "Not logged in", False, 403