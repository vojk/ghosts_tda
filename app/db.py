import sqlite3

import os

databaseExists = os.path.exists('./dbs/database.db')

if not databaseExists:  # ověřuje existenci databáze - zda-li existuje soubor database.db tak se nebude tvořit znova celá tabulka
    connection = sqlite3.connect('./dbs/database.db')  # připojí se a případně vytvoří databázi ./dbs/database.db
    with open('./dbs/schema.sql') as f:  # Vytvoří tabulku podle ./dbs/schema.sql
        connection.executescript(f.read())

    cur = connection.cursor()  # Vytvoří kursor
    connection.commit()  # vloží data do databáze
    connection.close()  # Uzavře spojení s databází


def get_db_connection():
    conn = sqlite3.connect('./dbs/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def read_data_from_db(table):  # čte data z databáze
    conn = sqlite3.connect('./dbs/database.db')
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM ' + table).fetchall()
    conn.close()
    return posts
