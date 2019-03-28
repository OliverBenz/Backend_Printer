import mysql.connector
from flask import Flask, request, jsonify
import json

import prints, status, user
import postQueue

app = Flask(__name__)

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

def get(db, cursor, tablename):
    if tablename == 'prints':
        return prints.get(db, cursor)
    if tablename == 'status':
        return status.get(db, cursor)



# ------------------------------------------------------------------------


@app.route('/<tablename>', defaults={'value': None})
@app.route('/<tablename>/<value>', methods=['GET'])
def general(tablename, value):
    db, cursor = conDB()
    
    result = {
        "data": []
    }

    if request.method == 'GET':
        result["data"] = get(db, cursor, tablename)
    else:
        print("Error. Invalid method")
    
    cloDB(db)
    return jsonify(result)

@app.route('/add', methods=['POST'])
def addPrint():
    db, cursor = conDB()
    # Filename:     filename-name-time-length-weight-price-usrid-amount-date-date_till
    obj = request.get_json()
    # TODO: Format filename and add to tables
    postQueue.newPrint(db, cursor, obj)

    cloDB(db)
    return ""

@app.route('/login/<info>', methods=['GET'])
def login(info):
    db, cursor = conDB()

    user.login(db, cursor, info)

    cloDB(db)

# Main
if __name__ == "__main__":
    app.run()