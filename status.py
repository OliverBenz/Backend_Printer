def get(db, cursor):
    sql = "SELECT * FROM status"
    cursor.execute(sql)
    result = cursor.fetchall()
    status = []

    # TODO: Move into a datapreparer Function
    for row in result:
        data = {
            "id": row[0],
            "name": row[1]
        }
        status.append(data)

    return status