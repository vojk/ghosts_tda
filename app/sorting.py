from datetime import datetime

import db
import app

sortTypes = ('dates', 'time_in_minutes', 'programming_lang', 'rating', 'None')


# kontroluje stav proměných zdali jsou prázdné tak dá default hodnotu, když není tak to jenom připraví na passnutí dál
def pre_sort(f_sort_type, f_filter_rating, f_filter_proglangs, f_filter_dates, f_filter_timeinminutes,
             f_filter_programmer, f_filter_categories,
             user_id):
    print("Kategorie:" + str(f_filter_categories))
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
    if f_filter_dates is None or f_filter_dates == "" or f_filter_dates == ",":
        f_filter_dates_min = '2000-01-01'
        f_filter_dates_max = datetime.today().date()
    else:
        print('else')
        f_filter_dates = f_filter_dates.split(",")
        print(len(f_filter_dates))
        if 0 < len(f_filter_dates):
            f_filter_dates_min = f_filter_dates[0]
        else:
            f_filter_dates_min = 'NULL'
        if 1 < len(f_filter_dates):
            if f_filter_dates[1] != "":
                f_filter_dates_max = f_filter_dates[1]
            else:
                f_filter_dates_max = datetime.today().date()
        else:
            f_filter_dates_max = datetime.today().date()
        print(str(f_filter_dates_min) + "MAX: " + str(f_filter_dates_max))
    if f_filter_timeinminutes is None or f_filter_timeinminutes == "":
        f_filter_timeinminutes_max = "NULL"
        f_filter_timeinminutes_min = '0'
    else:
        f_filter_timeinminutes = f_filter_timeinminutes.split(",")
        print(f_filter_timeinminutes)
        if 0 < len(f_filter_timeinminutes):
            f_filter_timeinminutes_min = f_filter_timeinminutes[0]
        else:
            f_filter_timeinminutes_max = 'NULL'
        if 1 < len(f_filter_timeinminutes):
            f_filter_timeinminutes_max = f_filter_timeinminutes[1]
        else:
            f_filter_timeinminutes_min = '0'
        if f_filter_timeinminutes_min == "":
            f_filter_timeinminutes_min = "0"
        if f_filter_timeinminutes_max == "":
            f_filter_timeinminutes_max = "NULL"
    if f_filter_programmer is None or f_filter_programmer == "" or f_filter_programmer == "None":
        conn = db.get_db_connection()
        users = conn.execute("SELECT id FROM users").fetchall()
        conn.close()
        print(f_filter_programmer)
        f_filter_programmer = ','.join([str(user[0]) for user in users])
        f_filter_programmer = f_filter_programmer.split(',')
    else:
        f_filter_programmer = [f_filter_programmer]
    if f_filter_categories is None or f_filter_categories == "":
        conn = db.get_db_connection()
        category_id = conn.execute("SELECT category_id FROM categories_records").fetchall()
        conn.close()
        f_filter_categories = ','.join([str(category_id_[0]) for category_id_ in category_id])
        f_filter_categories = f_filter_categories.split(',')
    elif f_filter_categories == "NULL":
        f_filter_categories = ['']
    else:
        f_filter_categories_temp = f_filter_categories.split(",")
        f_filter_categories = []
        for x in f_filter_categories_temp:
            f_filter_categories.append(x)

    print("Kategorie " + str(f_filter_categories))

    return sorting(f_sort_type, f_filter_timeinminutes_min, f_filter_timeinminutes_max, f_filter_rating_min,
                   f_filter_rating_max, f_filter_proglangs,
                   f_filter_dates_min, f_filter_dates_max, f_filter_programmer, f_filter_categories, user_id)


# sortuje data a pak je posílá do frontendu, když je zavolán
def sorting(sorting_parameter, f_filter_timeinminutes_min, f_filter_timeinminutes_max, f_filter_rating_min,
            f_filter_rating_max, proglangs, f_filter_dates_min,
            f_filter_dates_max, f_filter_programmer, f_filter_categories, user_id):
    print(f_filter_categories)
    conn = db.get_db_connection()
    cursor = conn.cursor()
    f_filter_programmer = f_filter_programmer
    placeholders = ','.join(['?'] * len(proglangs))
    placeholders_sort = ','.join([x['sortTypes'] for x in sorting_parameter])
    placeholders_categories = ','.join(['?'] * len(f_filter_categories))
    placeholders_programmers = ','.join(['?'] * len(f_filter_programmer))
    query = f"SELECT DISTINCT records.*, categories.category " \
            f"FROM records  " \
            f"LEFT JOIN categories_records ON records.id=categories_records.record_id " \
            f"LEFT JOIN categories ON categories.id=categories_records.category_id " \
            f"WHERE timeInMinutes BETWEEN ? AND ? AND (rating BETWEEN ? AND ? OR rating IS NULL) AND programmingLang IN ({placeholders}) AND dates BETWEEN ? AND ? " \
            f"AND category_id IN ({placeholders_categories}) AND records.user_id = {user_id} " \
            f"GROUP BY records.id " \
            f"ORDER BY {placeholders_sort}"
    print(query)
    values = [f_filter_timeinminutes_min, f_filter_timeinminutes_max, f_filter_rating_min, f_filter_rating_max] + [
        d['progLangs'] for d in proglangs] + [
                 f_filter_dates_min, f_filter_dates_max] + [x for x in f_filter_categories]
    records = cursor.execute(query, values).fetchall()

    print([x for x in f_filter_categories])
    cursor.close()
    conn.close()
    return records
