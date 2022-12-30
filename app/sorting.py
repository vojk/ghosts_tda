import db
import re

import sqlite3

sortTypes = ('dates', 'time_in_minutes', 'programming_lang', 'rating', 'None')


def sort(records_, sort_parameter_cut):
    reverse = False

    if len(sort_parameter_cut) >= 2:
        if sort_parameter_cut[1] == 'T':
            reverse = True
        else:
            reverse = False

    # Sortování pomocí SQL => Neohrabané až moc složité pro tuhle aplikaci ale ne nemožné
    # if sortParameter != 'None':
    #     conn = db.get_db_connection()
    #     records = conn.execute('SELECT * FROM ' + table + ' ORDER BY ' + sortParameter + ' DESC').fetchall()
    #     conn.close()
    # else:
    #     records = db.read_data_from_db(table)

    if sort_parameter_cut[0] != 'None':
        match sort_parameter_cut[0]:
            case 'dates':
                sorted_records = sorted(records_, key=lambda x: x[1], reverse=reverse)
                return sorted_records
            case 'time_in_minutes':
                sorted_records = sorted(records_, key=lambda x: x[2], reverse=reverse)
                return sorted_records
            case 'programming_lang':
                sorted_records = sorted(records_, key=lambda x: x[3], reverse=reverse)
                return sorted_records
            case 'rating':
                sorted_records = sorted(records_, key=lambda x: x[4], reverse=reverse)
                return sorted_records
    return records_


def filter_records(rating, proglangs, dates, timeinminutes, table, sort_parameter):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM " + table + " WHERE programmingLang IN ({}) " \
                                       "AND rating BETWEEN ? AND ? AND dates BETWEEN ? AND ? AND timeInMinutes BETWEEN 0 AND ?"

    placeholders = ",".join(["?"] * len(proglangs))
    query = query.format(placeholders)

    cursor.execute(query, tuple(proglangs) + (rating[0], rating[1]) + (dates[0], dates[1]) + tuple(timeinminutes))
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return sort(records, sort_parameter)
