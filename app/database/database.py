import sqlite3
import os

DATABASE = 'database.db'
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATABASE)

conn = None

def connect():
    global conn
    conn = sqlite3.connect(path)
    return conn

def execute(sql, data=None):
    global conn
    cursor = conn.cursor()

    if data != None:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    conn.commit()

def close():
    conn.close()
