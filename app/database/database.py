import sqlite3
import os

DATABASE = 'database.db'
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATABASE)

conn = None

def connect():
    global conn
    conn = sqlite3.connect(path)
    return conn

def insert(sql, data=None):
    global conn
    cursor = conn.cursor()
    if data != None:
        if type(data) == list:
            cursor.executemany(sql, data)
        else: 
            cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    last_id = cursor.lastrowid
    conn.commit()

    return last_id

def execute(sql, data=None):
    global conn
    cursor = conn.cursor()

    if data != None:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    values = cursor.fetchall()
    conn.commit()

    return values

def close():
    conn.close()
