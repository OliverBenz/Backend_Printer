import mysql.connector
from flask import Flask, request, jsonify
import json

import prints

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

def post(db, cursor, tablename, value):
    if tablename == 'prints':
        return "Error: Can't post directly into Prints"

@app.route('/<tablename>', defaults={'value': None})
@app.route('/<tablename>/<value>', methods=['GET', 'POST'])
def general(tablename, value):
    db, cursor = conDB()
    
    result = ""
    if request.method == 'GET':
        result = get(db, cursor, tablename)
    elif request.method == 'POST':
        post(db, cursor, tablename, value)

    cloDB(db)
    return str(result)

# Main
if __name__ == "__main__":
    app.run()