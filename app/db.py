import sqlite3

connection = sqlite3.connect('./dbs/database.db')  # připojí se a případně vytvoří databázi ./dbs/database.db

with open('./dbs/schema.sql') as f:  # Vytvoří tabulku podle ./dbs/schema.sql
    connection.executescript(f.read())

cur = connection.cursor()

connection.close()  # Uzavře spojení s databází
