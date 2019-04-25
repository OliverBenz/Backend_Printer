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
            "filename": row[1],
            "name": row[2],
            "time": row[3],
            "length": row[4],
            "weight": row[5]
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

        for row in result:
            print(row)
            data = {
                "filename": row[1],
                "name": row[2],
                "time": row[3],
                "timeReal": row[4],
                "length": row[5],
                "weight": row[6],
                "jobId": row[7],
                "spoolId": row[9],
                "amount": row[10],
                "date": row[12].strftime('%Y-%m-%d'),
                "dateUntil": "",
                "dateDone": "",
                "notes": row[15]
            }
            if row[13]:
                data["dateUntil"] = row[13].strftime('%Y-%m-%d')
            if row[14]:
                data["dateDone"] = row[14].strftime('%Y-%m-%d')
    
            prints.append(data)

        return prints, True, 200

    return "Not logged in", False, 403


def postJob(db, cursor, obj):
    # ----- Check if user is logged in -----
    if user.checkLoggedIn(cursor, obj["sessionId"]):
        
        # ----- Check if filename already exists -----
        sql = "SELECT count(id) from print WHERE filename = '%s'" % obj["filename"]
        cursor.execute(sql)

        printId = 0
        # ----- If Filename exsts: getId - If not: insert -----
        if cursor.fetchall()[0][0] > 0:
            sql = "SELECT id from print WHERE filename = '%s'" % obj["filename"]
            cursor.execute(sql)
            printId = cursor.fetchall()[0][0]
        else:
            # ----- Add Print -----
            fd = open('scripts/post/print.sql', 'r')
            sql = fd.read()
            fd.close()
            
            val = (obj["filename"], obj["name"], obj["time"], 0.00, obj["length"], obj["weight"])
            
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


def changeJobStatus(db, cursor, info):
    # Info: ---- sessionId, jobId, status ----
    if info["status"] == "to-do":
        info["status"] = "To Do"

    # get group and status of user
    uGroup = user.checkUserGroup(cursor, info["sessionId"])
    uStatus = user.checkUserStatus(cursor, info["sessionId"])

    # Check if the user is allowed to make the change
    if uGroup == "Registered" or uStatus == "Deactivated":
        return "Not allowed", False, 403
    elif uGroup != "Administrator" and uStatus == "Active":
        print("case")
        stat, code = user.checkJobSession(cursor, info["jobId"], info["sessionId"])
        if stat == False:
            return "Can't change job", stat, code
    else:
        if uGroup != "Administrator":
            return "Unexpected Case", False, 500


    # User can only change status Removed, to-do
    # Admin can change all status
    if uGroup == "User":
        if info["status"] != "to-do" and info["status"] != "removed":
            return "Change not allowed", False, 403


    fd = open('scripts/put/jobStatus.sql', 'r')
    sql = fd.read() % (info["status"], info["jobId"])
    fd.close()

    cursor.execute(sql)

    if cursor.rowcount == 1:
        db.commit()
        return "Successfully changed status", True, 200
    else:
        return "Could not change status", False, 500


def calcPrice(db, cursor, data):
    sql = "SELECT weight, price FROM spool WHERE id='%s'" % data["spoolId"]
    cursor.execute(sql)

    spool = cursor.fetchall()
    # price = (spool.price / spool.weight) * print.weight
    price = (float(spool[0][1]) / float(spool[0][0])) * float(data["printWeight"])

    return str(round(price, 2)), True, 200