import mysql.connector
from flask import Flask, request, jsonify
import json

import prints, status
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

def post(db, cursor, tablename, value):
    if tablename == 'prints':
        return "Error: Can't post directly into Prints"


# ------------------------------------------------------------------------


@app.route('/<tablename>', defaults={'value': None})
@app.route('/<tablename>/<value>', methods=['GET', 'POST'])
def general(tablename, value):
    db, cursor = conDB()
    
    result = {
        "data": []
    }

    if request.method == 'GET':
        result["data"] = get(db, cursor, tablename)
    elif request.method == 'POST':
        post(db, cursor, tablename, value)
    
    cloDB(db)
    return jsonify(result)

@app.route('/add/<filename>', methods=['POST'])
def addPrint(filename):
    db, cursor = conDB()
    # Filename:     filename-name-time-length-weight-price-usrid-amount-date-date_till

    # TODO: Format filename and add to tables
    postQueue.newPrint(db, cursor, filename)

    cloDB(db)
    return ""


# Main
if __name__ == "__main__":
    app.run()