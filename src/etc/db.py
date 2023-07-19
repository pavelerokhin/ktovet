import sqlite3
import os


def create_db(db_name, schema):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(schema)
    db.commit()
    db.close()


def delete_db(db_name):
    os.remove(db_name)


def execute_query(db_name, query):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()
