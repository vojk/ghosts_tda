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


def app_wind():
    sort_type = request.args.get('sort', default=None, type=str)
    filter_rating = request.args.get('rating', default=None, type=str)
    filter_proglangs = request.args.get('proglang', default=None, type=str)
    filter_dates = request.args.get('date', default=None, type=str)
    filter_timeinminutes = request.args.get('time', default=None, type=str)

    return render_template('update.html',
                           text=sorting.pre_sort(sort_type, filter_rating, filter_proglangs, filter_dates,
                                                 filter_timeinminutes, None))


@app.route('/app', methods=["GET", "POST"])
def app_wind():
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('records.html', texts=sorting.pre_sort(None, None, None, None,
                                                                  None, None), defs=proglangs, programmers=programmers)


@app.route('/sort')
def sort():
    sort_field = request.args.get('sort_field')
    filter_rating = request.args.get('filter_rating')
    filter_formatted_date = request.args.get('filter_formatted_date')
    filter_programmingLangs = request.args.get('filter_programmingLangs')
    filter_time = request.args.get('filter_time')
    filter_programmer = request.args.get('filter_programmer')
    print(sort_field)
    return render_template('table_records.html',
                           texts=sorting.pre_sort(sort_field, filter_rating, filter_programmingLangs,
                                                  filter_formatted_date,
                                                  filter_time, filter_programmer))


@app.route("/add/", methods=('GET', 'POST'))  # přidání záznamu
@app.route('/app/add/', methods=('GET', 'POST'))
def create_record():
    if request.method == 'POST':
        date = request.form['formDate']
        minutes = request.form['formMinutes']
        rating = request.form['formRating']
        progLang = request.form['formProgLang_select']
        desc = request.form['formDesc']
        programmer = request.form['formProgrammer_select']

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
            programmer_id = db.get_id_of_user(programmer)
            print(programmer_id[0][0])
            conn.execute(
                'INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, programmer, programmerId) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (date, minutes, progLang, rating, desc, programmer, programmer_id[0][0]))
            conn.commit()
            conn.close()
            return redirect(url_for('app_wind'))
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('createWind.html', defs=proglangs, programmers=programmers)


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))  # úprava záznamu
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


@app.route('/<int:id>/delete/', methods=('GET', 'POST'))  # samže záznam
@app.route('/app/<int:id>/delete/', methods=('GET', 'POST'))
def delete(id):
    if request.method == "POST":
        print(id)
        record = db.get_data_from_db_by_id(id)
        if not record:
            abort(404)

        conn = db.get_db_connection()
        conn.execute('DELETE FROM records WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    return render_template('removeWarn.html')


@app.route('/user/add', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_add_user():
    if request.method == "POST":
        username = request.form['form_username']
        conn = db.get_db_connection()
        conn.execute(
            'INSERT INTO users (programmer) '
            'VALUES (?)', (username,))
        conn.commit()
        conn.close()
    return render_template('createUserWind.html', username="")


@app.route('/user/<string:username>/edit', methods=["GET", "POST"])  # funkce pro upravení uživatele
def app_edit_user(username):
    programmer_id = db.get_id_of_user(username)
    if request.method == "POST":
        new_username = request.form['form_username']
        conn = db.get_db_connection()
        conn.execute("BEGIN TRANSACTION")
        try:
            conn.execute(
                'UPDATE users SET programmer = ? WHERE id = ?',
                (new_username, programmer_id[0][0],))
            conn.execute('UPDATE records SET programmer = ? WHERE programmerId = ?',
                         (new_username, programmer_id[0][0],))
            conn.execute("COMMIT")
        except:
            conn.execute("ROLLBACK")
            raise
        conn.close()
        return redirect(url_for('app_wind'))
    conn = db.get_db_connection()
    username = conn.execute("SELECT programmer FROM users WHERE id IS ?", (programmer_id[0][0],)).fetchall()
    conn.close()
    return render_template('createUserWind.html', username=username[0][0])


@app.route('/user/<string:username>/delete', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_delete_user(username):
    username = username
    conn = db.get_db_connection()
    programmer_id = db.get_id_of_user(username)
    conn.execute('DELETE FROM records WHERE programmerId = ?', (programmer_id[0][0],))
    conn.execute('DELETE FROM users WHERE id = ?', (programmer_id[0][0],))
    conn.commit()
    conn.close()
    return redirect(url_for('app_wind'))


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run()

# TODO okomentovat kod!!!