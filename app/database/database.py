import sqlite3
import os

DATABASE = 'database.db'
database_full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATABASE)

class Database:
    def __init__(self) :
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(database_full_path)
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    def insert(self, sql, data=None):
        cursor = self.conn.cursor()

        if data != None:
            if type(data) == list:
                cursor.executemany(sql, data)
            else: 
                cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        last_id = cursor.lastrowid
        self.conn.commit()

        return last_id

    def execute(self, sql, data=None):
        cursor = self.conn.cursor()

        if data != None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        values = cursor.fetchall()
        self.conn.commit()

        return values

    def close(self):
        self.conn.close()

db = Database()