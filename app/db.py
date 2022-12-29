import sqlite3
from flask import abort

import os

user = "default"  # základní uživatel

databasePath = ''

if os.name == 'posix':
    databasePath = 'app/dbs/database.db'
elif os.name == 'nt':
    databasePath = './dbs/database.db'

databaseExists = os.path.exists(databasePath)

if not databaseExists:  # ověřuje existenci databáze - zda-li existuje soubor database.db tak se nebude tvořit znova celá tabulka
    connection = sqlite3.connect(databasePath)  # připojí se a případně vytvoří databázi ./dbs/database.db
    connection.executescript(
        'CREATE TABLE ' + "u_" + user +
        ' (id INTEGER PRIMARY KEY AUTOINCREMENT, dates DATE NOT NULL, timeInMinutes INT NOT NULL, '
        'programmingLang TEXT NOT NULL, rating INT NOT NULL, description TEXT NOT NULL)')

    cur = connection.cursor()  # Vytvoří kursor
    connection.commit()  # vloží data do databáze
    connection.close()  # Uzavře spojení s databází


def get_db_connection():
    conn = sqlite3.connect(databasePath)
    conn.row_factory = sqlite3.Row
    return conn


def read_data_from_db(table):  # čte data z databáze
    conn = sqlite3.connect(databasePath)
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM ' + table).fetchall()
    conn.close()
    return posts


def get_data_from_db_by_id(table, post_id):  # čte data z databáze
    conn = get_db_connection()
    record = conn.execute('SELECT * FROM ' + table + ' WHERE id = ?',
                          (post_id,)).fetchall()
    conn.close()
    return record


def create_user(user):
    conn = get_db_connection()
    if not user:
        print("No User Found")
    else:
        conn.executescript(
            'CREATE TABLE ' + "u_" + user +
            ' (id INTEGER PRIMARY KEY AUTOINCREMENT, dates DATE NOT NULL, timeInMinutes INT NOT NULL, '
            'programmingLang TEXT NOT NULL, rating INT NOT NULL, description TEXT NOT NULL)')
        conn.commit()
        conn.close()