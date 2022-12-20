import sqlite3

connection = sqlite3.connect('./dbs/database.db')  # připojí se a případně vytvoří databázi ./dbs/database.db

with open('./dbs/schema.sql') as f:  # Vytvoří tabulku podle ./dbs/schema.sql
    connection.executescript(f.read())

cur = connection.cursor()  # Vytvoří kursor

cur.execute(
    "INSERT INTO trenink VALUES (1, 2052020, 50, 'Java', 4, 'TestDesc')")  # nastaví do listu data, která se pak vloží do databáze
connection.commit()  # vloží data do databáze

connection.close()  # Uzavře spojení s databází


def readDataFromDb():  # čte data z databáze
    conn = sqlite3.connect('./dbs/database.db')
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM trenink').fetchall()
    conn.close()
    return posts
