import mysql.connector
from flask import Flask, request, jsonify
import json

import queue, postPrint, status, user, history

app = Flask(__name__)
httpHeaders = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE",
}

# ------------------------------------------------------------------------


@app.route('/<tablename>', defaults={'value': None})
@app.route('/<tablename>/<value>', methods=['GET'])
def general(tablename, value):
    db, cursor = conDB()
    
    result = { "data": [] }

    if request.method == 'GET':
        result["data"] = get(db, cursor, tablename, value)
    else:
        print("Error. Invalid method")
    
    cloDB(db)
    return jsonify(result)


@app.route('/add', methods=['POST'])
def addPrint():
    db, cursor = conDB()
    # Filename:     usrid-amount-date-date_till-filename-name-time-length-weight-price

    # TODO: Format filename and add to tables
    postPrint.newPrint(db, cursor, request.json)

    cloDB(db)
    return ""


@app.route('/user/login', methods=['POST'])
def login():
    db, cursor = conDB()

    sessionId = user.login(db, cursor, request.json)

    cloDB(db)
    return sessionId


@app.route('/user/changepw', methods=['POST'])
def changePassword():
    db, cursor = conDB()

    # Get sessionId, password to verify that the user is logged in and knows the password
    # return new sessionId so the user can stay logged in
    sessionId = user.login(db, cursor, request.json)

    cloDB(db)
    return '{"sessionId": %s}' % sessionId

@app.route('/user/history/<sessionId>', methods=['GET'])
def getUserHistory(sessionId):
    db, cursor = conDB()

    result = { "data": [] }
    result["data"] = history.getUserHistory(db, cursor, sessionId)

    cloDB(db)
    return jsonify(result)
# ------------------------------------------------------------------------


def conDB():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="3d_printer"
    )
    cursor = db.cursor()

    return db, cursor

def cloDB(db):
    db.close()

def get(db, cursor, tablename, value):
    if tablename == 'queue':
        return queue.get(db, cursor, value)
    if tablename == 'status':
        return status.get(db, cursor)


# Main
if __name__ == "__main__":
    app.run()