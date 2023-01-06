from datetime import datetime

import db
import app

sortTypes = ('dates', 'time_in_minutes', 'programming_lang', 'rating', 'None')


def pre_sort(f_sort_type, f_filter_rating, f_filter_proglangs, f_filter_dates, f_filter_timeinminutes):
    if f_sort_type is None or f_sort_type == "":
        f_sort_type = [{'sortTypes': 'NULL'}]
    else:
        f_sort_type = f_sort_type.replace('_', ' ')
        f_sort_type_temp = f_sort_type.split(',')
        f_sort_type = []
        for x in f_sort_type_temp:
            f_sort_type.append({'sortTypes': x})
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

    return sorting(f_sort_type, f_filter_timeinminutes, f_filter_rating_min, f_filter_rating_max, f_filter_proglangs,
                   f_filter_dates_min, f_filter_dates_max)


def sorting(sorting_parameter, time_in_minutes, f_filter_rating_min, f_filter_rating_max, proglangs, f_filter_dates_min,
            f_filter_dates_max):
    print(f_filter_rating_min)
    print(f_filter_rating_max)
    conn = db.get_db_connection()
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(proglangs))
    placeholders_sort = ','.join([x['sortTypes'] for x in sorting_parameter])
    query = f"SELECT * " \
            f"FROM records " \
            f"WHERE timeInMinutes BETWEEN 0 AND ? AND (rating BETWEEN ? AND ? OR rating IS NULL) AND programmingLang IN ({placeholders}) AND dates BETWEEN ? AND ? " \
            f"ORDER BY {placeholders_sort}"
    values = [time_in_minutes, f_filter_rating_min, f_filter_rating_max] + [
        d['progLangs'] for d in proglangs] + [
                 f_filter_dates_min, f_filter_dates_max]
    records = cursor.execute(query, values).fetchall()
    cursor.close()
    conn.close()
    return records
