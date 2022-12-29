import db

import sqlite3


def sort(sortParameter, table):
    conn = db.get_db_connection()
    records = conn.execute('SELECT * FROM ' + table + ' ORDER BY ' + sortParameter + '').fetchall()
    conn.close()
    return records
