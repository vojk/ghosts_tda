from datetime import datetime

import db
import app

sortTypes = ('dates', 'time_in_minutes', 'programming_lang', 'rating', 'None')


def pre_sort(f_sort_type, f_filter_rating, f_filter_proglangs, f_filter_dates, f_filter_timeinminutes, f_sort_rule):
    if f_sort_type is None or f_sort_type == "":
        f_sort_type = 'NULL'
    if f_sort_rule is None or f_sort_rule == "" or f_sort_rule == 'ASC':
        f_sort_rule = 'ASC'
    elif f_sort_rule == 'DESC':
        f_sort_rule = 'DESC'
    if f_filter_rating is None or f_filter_rating == "":
        f_filter_rating_min = '0'
        f_filter_rating_max = '5'
    else:
        f_filter_rating = f_filter_rating.split(",")
        f_filter_rating.sort()
        if 0 < len(f_filter_rating):
            f_filter_rating_min = f_filter_rating[0]
        else:
            f_filter_rating_min = 'NULL'
        if 1 < len(f_filter_rating):
            f_filter_rating_max = f_filter_rating[1]
        else:
            f_filter_rating_max = 'NULL'
    if f_filter_proglangs is None or f_filter_proglangs == "":
        f_filter_proglangs = app.proglangs
    else:
        f_filter_proglangs_temp = f_filter_proglangs.split(",")
        f_filter_proglangs = []
        for x in f_filter_proglangs_temp:
            f_filter_proglangs.append({'progLangs': x})
        print(f_filter_proglangs)
    if f_filter_dates is None or f_filter_dates == "":
        f_filter_dates_min = '2000-01-01'
        f_filter_dates_max = datetime.today().date()
    else:
        print('else')
        f_filter_dates = f_filter_dates.split(",")
        f_filter_dates.sort()
        if 0 < len(f_filter_dates):
            f_filter_dates_min = f_filter_dates[0]
        else:
            f_filter_dates_min = 'NULL'
        if 1 < len(f_filter_dates):
            f_filter_dates_max = f_filter_dates[1]
        else:
            f_filter_dates_max = datetime.today().date()
    if f_filter_timeinminutes is None or f_filter_timeinminutes == "":
        f_filter_timeinminutes = 'NULL'

    print('min: ' + f_filter_dates_min)
    return sorting(f_sort_type, f_filter_timeinminutes, f_filter_rating_min, f_filter_rating_max, f_filter_proglangs,
                   f_filter_dates_min, f_filter_dates_max, f_sort_rule)


def sorting(sorting_parameter, time_in_minutes, f_filter_rating_min, f_filter_rating_max, proglangs, f_filter_dates_min,
            f_filter_dates_max, f_sort_rule):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(proglangs))
    query = f"SELECT * FROM u_default WHERE timeInMinutes BETWEEN 0 AND ? AND (rating BETWEEN ? AND ? OR rating IS NULL) AND programmingLang IN ({placeholders}) AND dates BETWEEN ? AND ? ORDER BY {sorting_parameter} {f_sort_rule}"
    values = [time_in_minutes, f_filter_rating_min, f_filter_rating_max] + [d['progLangs'] for d in proglangs] + [
        f_filter_dates_min, f_filter_dates_max]
    records = cursor.execute(query, values).fetchall()

    print(records)

    cursor.close()
    conn.close()
    return records


# ----Useless část kodu----

def sort(records_, sort_parameter_cut):
    reverse = False

    if len(sort_parameter_cut) >= 2:
        if sort_parameter_cut[1] == 'T':
            reverse = True
        else:
            reverse = False

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


def test_of_sort(sort_parameter):
    reverse = False
    if not sort_parameter is None:
        match sort_parameter:
            case 'dates':
                sorted_records = sorted(db.read_data_from_db('u_default'), key=lambda x: x[1], reverse=reverse)
                return sorted_records
            case 'time_in_minutes':
                sorted_records = sorted(db.read_data_from_db('u_default'), key=lambda x: x[2], reverse=reverse)
                return sorted_records
            case 'programming_lang':
                sorted_records = sorted(db.read_data_from_db('u_default'), key=lambda x: x[3], reverse=reverse)
                return sorted_records
            case 'rating':
                sorted_records = sorted(db.read_data_from_db('u_default'), key=lambda x: x[4], reverse=reverse)
                return sorted_records
    else:
        return db.read_data_from_db('u_default')


def filter_records(rating, proglangs, dates, timeinminutes, table, sort_parameter):
    if timeinminutes == 'None':
        timeinminutes = ["200"]
    if dates == 'None' or dates[1] is None:
        dates = ["2000-01-01", datetime.today().strftime('%Y-%m-%d')]
    if proglangs == 'None':
        proglangs = app.proglangs
    if timeinminutes == 'None':
        timeinminutes = ["0", "500"]
    print(rating)
    print(proglangs)
    print(dates)
    print(timeinminutes)
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
