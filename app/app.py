import datetime
import re

from flask import Flask, render_template, request, flash, redirect, url_for, abort
import db
import secrets
import sorting

proglangs = [{'progLangs': 'JAVA'}, {'progLangs': 'PYTHON'}, {'progLangs': 'Csharp'}]

app = Flask(__name__)

db  # inicializuje databázi


@app.route('/')
def index():
    return redirect(url_for('app_wind'))


@app.route('/app', methods=["GET", "POST"])
def app_wind():
    sort_type = request.args.get('sort', default=None, type=str)
    filter_rating = request.args.get('rating', default=None, type=str)
    filter_proglangs = request.args.get('proglang', default=None, type=str)
    filter_dates = request.args.get('date', default=None, type=str)
    filter_timeinminutes = request.args.get('time', default=None, type=str)

    return render_template('update.html',
                           text=sorting.pre_sort(sort_type, filter_rating, filter_proglangs, filter_dates,
                                                 filter_timeinminutes))


# BackgroundTask
@app.route('/background_process_test')
def background_process_test():
    print("Hello")
    return "nothing"


@app.route("/blank")
def blank_site():
    return render_template('update.html', text=db.read_data_from_db())


@app.route("/add/", methods=('GET', 'POST'))
@app.route('/app/add/', methods=('GET', 'POST'))
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
                'INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, programmer) '
                'VALUES (?, ?, ?, ?, ?, ?)', (date, minutes, progLang, rating, desc, 'u_default'))
            conn.commit()
            conn.close()
            return redirect(url_for('app_wind'))

    return render_template('createWind.html', defs=proglangs)


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
@app.route('/app/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    record = db.get_data_from_db_by_id(id)
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
                'UPDATE records SET dates = ?, timeInMinutes = ?, programmingLang = ?, rating = ?, description = ? '
                'WHERE id = ?',
                (date, minutes, progLang, rating, desc, id))
            conn.commit()
            conn.close()
            return redirect(url_for('app_wind'))

    return render_template('editWind.html', record=record, defs=proglangs)


@app.route('/<int:id>/delete/', methods=('GET', 'POST'))
@app.route('/app/<int:id>/delete/', methods=('GET', 'POST'))
def delete(id):
    record = db.get_data_from_db_by_id(id)
    if not record:
        abort(404)

    conn = db.get_db_connection()
    conn.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('app_wind'))


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run()
