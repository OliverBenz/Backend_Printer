import mysql.connector
from flask import Flask, request, jsonify

import history

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="test"
)

cursor = mydb.cursor()