import sqlite3
from flask import abort

import os

user = "u_default"  # základní uživatel

databasePath = ''

if os.name == 'posix':
    databasePath = 'app/dbs/database.db'
elif os.name == 'nt':
    databasePath = './dbs/database.db'

databaseExists = os.path.exists(databasePath)

if not databaseExists:  # ověřuje existenci databáze - zda-li existuje soubor database.db tak se nebude tvořit znova celá tabulka
    with open('app/dbs/schemas/schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    connection = sqlite3.connect(databasePath)  # připojí se a případně vytvoří databázi ./dbs/database.db
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.executescript(sql_script)

    connection.commit()  # vloží data do databáze
    connection.close()  # Uzavře spojení s databází


def get_db_connection():  # napojení se na databázi
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


def get_id_of_user(username):
    conn = get_db_connection()
    query = "SELECT id FROM users WHERE users.username IS ?"
    values = [username]
    programmer_id = conn.execute(query, values).fetchall()
    conn.close()
    return programmer_id
