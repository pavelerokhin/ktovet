import sqlite3
import os


def create(db_name, schema):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(schema)
    db.commit()
    db.close()


def delete(db_name):
    os.remove(db_name)


def get_db(db_name):
    return sqlite3.connect(db_name)


def execute(db_name, query):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def execute_get_results(db_name, query):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()
    return cursor.fetchall()
