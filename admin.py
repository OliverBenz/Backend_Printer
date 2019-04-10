import user

def getQueue(db, cursor, status, sessionId):
    if status == "to-do":
        status = "To Do"
    
    if not user.checkLoggedIn(cursor, sessionId):
        return "Not logged in", False, 403
    elif not user.checkUserGroup(cursor, sessionId) == "Administrator":
        return "Not admin", False, 401
    else:
        fd = open('scripts/get/admin/job.sql', 'r')
        sql = fd.read() % status
        fd.close()

        cursor.execute(sql)
        result = cursor.fetchall()
        dataList = []

        # ID is jobId, not print
        for row in result:
            data = {
                "filename": row[0],
                "name": row[1],
                "time": row[2],
                "timeReal": row[3],
                "length": row[4],
                "weight": row[5],
                "price": row[6],
                "id": row[7],
                "date": row[8].strftime('%Y-%m-%d'),
                "dateUntil": "",
                "dateDone": "",
                "notes": row[11],
                "user": row[12],
                "status": row[13],
                "amount": row[14]
            }
            if row[9]:
                data["dateUntil"] = row[9].strftime('%Y-%m-%d')
            if row[10]:
                data["dateDone"] = row[10].strftime('%Y-%m-%d')

            dataList.append(data)
        return dataList, True, 200


def changeJob(db, cursor, info):
    if not user.checkLoggedIn(cursor, info["sessionId"]):
        return "Not logged in", False, 403
    elif not user.checkUserGroup(cursor, info["sessionId"]) == "Administrator":
        return "Not admin", False, 401
    else:
        # TODO: Get users
        return "Function not implemented yet", False, 400


def getUsers(db, cursor, status, sessionId):
    if not user.checkLoggedIn(cursor, sessionId):
        return "Not logged in", False, 403
    elif not user.checkUserGroup(cursor, sessionId) == "Administrator":
        return "Not admin", False, 401
    else:
        fd = open('scripts/get/admin/user.sql', 'r')
        sql = fd.read() % status
        fd.close()
        print(sql)

        cursor.execute(sql)
        result = cursor.fetchall()

        userList = []

        for row in result:
            userList.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "group": row[3]
            })
        return userList, True, 200 