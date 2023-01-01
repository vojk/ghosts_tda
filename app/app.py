import datetime
import re

from flask import Flask, render_template, request, flash, redirect, url_for, abort
import db
import secrets
import sorting

proglangs = [{'progLangs': 'JAVA'}, {'progLangs': 'PYTHON'}, {'progLangs': 'Csharp'}]

app = Flask(__name__)

db  # inicializuje databázi


# @app.route('/', methods=('GET', 'POST'))
# @app.route('/<string:sort>', methods=('GET', 'POST'))
# @app.route('/<string:sort>&<string:filters>', methods=('GET', 'POST'))
# def index(sort=None, filters=None):  # main code base
#     # http://127.0.0.1:5000/None&rating=0,5;proglang=JAVA,PYTHON,Csharp;Date=2022-03-14,2022-12-25;timeinminutes=200
#     maxminRating_f = 'None'
#     maxminDates_f = 'None'
#     timeinminutes_f = 'None'
#     prog_langs_f = 'None'
#     sort_parameter_cut = 'NULL'
#     if sort is not None:
#         sort_parameter_cut = re.findall('.[^A-Z]*', sort)
#     if sort is not None and sort_parameter_cut[0] in sorting.sortTypes:
#         # record = sorting.sort(sort, 'u_default')
#         if filters is not None:  # Filtry
#             seperatedfiltersWithWhiteSpaces = filters.split(";")  # Určení oddělovače
#             seperatedfilters = list(filter(None, seperatedfiltersWithWhiteSpaces))
#             if len(seperatedfilters) >= 1:
#                 maxminRating_f = seperatedfilters[0].split("=", 1)[1].split(
#                     ",")  # Oddělní maximálního a minimálního hodnocení
#             if len(seperatedfilters) >= 2:
#                 prog_langs_f = seperatedfilters[1].split("=", 1)[1].split(",")  # Oddělní programovacích jazyků
#             if len(seperatedfilters) >= 3:
#                 maxminDates_f = seperatedfilters[2].split("=", 1)[1].split(
#                     ",")  # Oddělní maximálního a minimálního data
#             if len(seperatedfilters) >= 4:
#                 timeinminutes_f = seperatedfilters[3].split("=", 1)[1].split(
#                     ",")  # čas strávený nad procvičováním
#             return render_template('update.html',
#                                    text=sorting.filter_records(maxminRating_f, prog_langs_f, maxminDates_f,
#                                                                timeinminutes_f, 'u_default',
#                                                                sort_parameter_cut))
#     elif sort_parameter_cut[0] not in sorting.sortTypes and sort is not None:
#         return redirect(url_for('index'))
#     return render_template('update.html', text=db.read_data_from_db('u_default'))

@app.route('/app', methods=["GET", "POST"])
def app_wind():
    sort_type = request.args.get('sort', default=None, type=str)
    sort_rule = request.args.get('r', default=None, type=str)
    filter_rating = request.args.get('rating', default=None, type=str)
    filter_proglangs = request.args.get('proglang', default=None, type=str)
    filter_dates = request.args.get('date', default=None, type=str)
    filter_timeinminutes = request.args.get('time', default=None, type=str)

    return render_template('update.html',
                           text=sorting.pre_sort(sort_type, filter_rating, filter_proglangs, filter_dates,
                                                 filter_timeinminutes, sort_rule))


# BackgroundTask
@app.route('/background_process_test')
def background_process_test():
    print("Hello")
    return "nothing"


@app.route("/blank")
def blank_site():
    return render_template('update.html', text=db.read_data_from_db('u_default'))


@app.route("/create/", methods=('GET', 'POST'))
def create_record():
    if request.method == 'POST':
        date = request.form['formDate']
        minutes = request.form['formMinutes']
        rating = request.form['formRating']
        progLang = request.form['formProgLang_select']
        desc = request.form['formDesc']

        if not date:
            print("No date found")
        elif not minutes or minutes == 0:
            print("No minutes found")
        elif progLang == "None" or not progLang:
            print("No progLang found")
        elif not desc:
            print("No desc found")
        else:
            conn = db.get_db_connection()
            conn.execute(
                'INSERT INTO u_default (dates, timeInMinutes, programmingLang, rating, description) '
                'VALUES (?, ?, ?, ?, ?)', (date, minutes, progLang, rating, desc))
            conn.commit()
            conn.close()
            return redirect(url_for('blank_site'))

    return render_template('createWind.html', defs=proglangs)


@app.route('/<username>/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id, username):
    record = db.get_data_from_db_by_id(username, id)
    if not record:
        abort(404)

    if request.method == 'POST':
        date = request.form['formDate']
        minutes = request.form['formMinutes']
        rating = request.form['formRating']
        progLang = request.form['formProgLang_select']
        desc = request.form['formDesc']

        if not date:
            print("No date found")
        elif not minutes or minutes == 0:
            print("No minutes found")
        elif progLang == "None" or not progLang:
            print("No progLang found")
        elif not desc:
            print("No desc found")
        else:
            conn = db.get_db_connection()
            conn.execute(
                'UPDATE ' + username +
                ' SET dates = ?, timeInMinutes = ?, programmingLang = ?, rating = ?, description = ? '
                'WHERE id = ?',
                (date, minutes, progLang, rating, desc, id))
            conn.commit()
            conn.close()
            return redirect(url_for('blank_site'))

    return render_template('editWind.html', record=record, defs=proglangs)


@app.route('/<username>/<int:id>/delete/', methods=('GET', 'POST'))
def delete(id, username):
    record = db.get_data_from_db_by_id(username, id)
    if not record:
        abort(404)

    conn = db.get_db_connection()
    conn.execute('DELETE FROM ' + username + ' WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('blank_site'))


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run()
