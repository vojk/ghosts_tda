import sqlite3
from flask import abort

import os

user = "records"  # základní uživatel

databasePath = ''

if os.name == 'posix':
    databasePath = 'app/dbs/database.db'
elif os.name == 'nt':
    databasePath = './dbs/database.db'

databaseExists = os.path.exists(databasePath)

if not databaseExists:  # ověřuje existenci databáze - zda-li existuje soubor database.db tak se nebude tvořit znova celá tabulka
    connection = sqlite3.connect(databasePath)  # připojí se a případně vytvoří databázi ./dbs/database.db
    connection.executescript(
        'CREATE TABLE records (id INTEGER PRIMARY KEY AUTOINCREMENT, dates DATE NOT NULL, timeInMinutes INT NOT NULL, '
        'programmingLang TEXT NOT NULL, rating INT NOT NULL, description TEXT NOT NULL, programmer TEXT NOT NULL)')
    connection.executescript(
        'CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, programmer TEXT NOT NULL)')

    cur = connection.cursor()  # Vytvoří kursor
    connection.commit()  # vloží data do databáze
    connection.close()  # Uzavře spojení s databází


def get_db_connection():
    conn = sqlite3.connect(databasePath)
    conn.row_factory = sqlite3.Row
    return conn


def read_data_from_db():  # čte data z databáze
    conn = sqlite3.connect(databasePath)
    conn.row_factory = sqlite3.Row
    records = conn.execute('SELECT * FROM records').fetchall()
    conn.close()
    return records


def get_data_from_db_by_id(post_id):  # čte data z databáze
    conn = get_db_connection()
    record = conn.execute('SELECT * FROM records WHERE id = ?',
                          (post_id,)).fetchall()
    conn.close()
    return record


def create_user(user):
    conn = get_db_connection()
    if not user:
        print("No User Found")
    else:
        conn.executescript(
            'CREATE TABLE records (id INTEGER PRIMARY KEY AUTOINCREMENT, dates DATE NOT NULL, timeInMinutes INT NOT NULL, '
            'programmingLang TEXT NOT NULL, rating INT NOT NULL, description TEXT NOT NULL, programmer TEXT NOT NULL)')
        conn.commit()
        conn.close()
