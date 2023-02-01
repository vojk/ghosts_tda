from flask import Flask, render_template, request, redirect, url_for, abort
import db
import secrets
import sorting

pre_proglangs = [{'progLangs': 'Java'}, {'progLangs': 'Python'}, {'progLangs': 'C'}, {'progLangs': 'Ruby'},
                 {'progLangs': 'JavaScript'}, {'progLangs': 'TypeScript'}, {'progLangs': 'Kotlin'}]

proglangs = sorted(pre_proglangs, key=lambda x: x['progLangs'])

app = Flask(__name__)

db  # inicializuje databázi


@app.route('/')
def index():
    return redirect(url_for('app_wind'))


@app.route('/app/', methods=["GET", "POST"])
def app_wind():
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    categorie = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template('records.html', texts=sorting.pre_sort(None, None, None, None,
                                                                  None, None, None), defs=proglangs,
                           programmers=programmers, categories=categorie)


@app.route('/sort')
def sort():
    sort_field = request.args.get('sort_field')
    filter_rating = request.args.get('filter_rating')
    filter_formatted_date = request.args.get('filter_formatted_date')
    filter_programmingLangs = request.args.get('filter_programmingLangs')
    filter_time = request.args.get('filter_time')
    filter_programmer = request.args.get('filter_programmer')
    filter_categories = request.args.get('filter_categories')
    print("pred " + str(filter_categories))
    print(sort_field)
    records = sorting.pre_sort(sort_field, filter_rating, filter_programmingLangs,
                               filter_formatted_date,
                               filter_time, filter_programmer, filter_categories)

    return render_template('customElements/table_row.html',
                           texts=sorting.pre_sort(sort_field, filter_rating, filter_programmingLangs,
                                                  filter_formatted_date,
                                                  filter_time, filter_programmer, filter_categories))


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
            cursor = conn.cursor()
            programmer_id = db.get_id_of_user(programmer)
            print(programmer_id[0][0])
            cursor.execute(
                'INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, programmer, programmerId) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (date, minutes, progLang, rating, desc, programmer, programmer_id[0][0]))
            conn.commit()
            last_id = cursor.lastrowid
            cursor.execute(
                'INSERT INTO categories_records (category_id, record_id) '
                'VALUES (?, ?)', ('NULL', last_id))
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
            conn.execute(
                'UPDATE records SET dates = ?, timeInMinutes = ?, programmingLang = ?, rating = ?, description = ?, programmer = ?, programmerId = ? '
                'WHERE id = ?',
                (date, minutes, progLang, rating, desc, programmer, programmer_id[0][0], id))
            conn.commit()
            conn.close()
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('editWind.html', record=record, defs=proglangs, programmers=programmers)


@app.route('/<int:id>/delete/', methods=('GET', 'POST'))  # samže záznam
@app.route('/app/<int:id>/delete/', methods=('GET', 'POST'))
def delete(id):
    if request.method == "POST":
        print("id " + str(id))
        record = db.get_data_from_db_by_id(id)
        if not record:
            abort(404)

        conn = db.get_db_connection()
        conn.execute('DELETE FROM records WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    return render_template('removeWarn.html')


@app.route('/user/add/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
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


@app.route('/app/user/<string:username>/add/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_add_user_save(username):
    if request.method == "POST":
        conn = db.get_db_connection()
        conn.execute(
            'INSERT INTO users (programmer) '
            'VALUES (?)', (username,))
        conn.commit()
        conn.close()
    return render_template('createUserWind.html', username="")


programmer_id = ""


@app.route('/app/user/<string:username>/edit/', methods=["GET", "POST"])
def app_edit_user_save(username):
    if request.method == "POST":
        new_username = username
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
    return 'show'


@app.route('/user/<string:username>/edit/', methods=["GET", "POST"])  # funkce pro upravení uživatele
def app_edit_user(username):
    global programmer_id
    programmer_id = db.get_id_of_user(username)
    conn = db.get_db_connection()
    username = conn.execute("SELECT programmer FROM users WHERE id IS ?", (programmer_id[0][0],)).fetchall()
    conn.close()
    return render_template('createUserWind.html', username=username[0][0])


@app.route('/user/<string:username>/delete/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_delete_user(username):
    if request.method == "POST":
        username = username
        conn = db.get_db_connection()
        programmer_id = db.get_id_of_user(username)
        conn.execute('DELETE FROM records WHERE programmerId = ?', (programmer_id[0][0],))
        conn.execute('DELETE FROM users WHERE id = ?', (programmer_id[0][0],))
        conn.commit()
        conn.close()
    return render_template('removeWarn.html')


@app.route('/user/delete/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_delete_user_wind():
    return render_template('removeWarn.html')


@app.route('/app/appUpt/updateUserList', methods=["GET", "POST"])
def update_user_list():
    conn = db.get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('customElements/tableForUsers.html', users=users)


@app.route('/app/user/', methods=["GET", "POST"])
def users_overview():
    conn = db.get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('usersOverview.html', users=users)


@app.route('/app/categories')
def categories_overview():
    conn = db.get_db_connection()
    categorie = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template('categoriesOverview.html', categories=categorie)


@app.route('/app/categories/add/', methods=["GET", "POST"])
def categories_add():
    if request.method == "POST":
        name_cat = request.form["form_name_category"]
        desc_cat = request.form["form_desc_category"]
        color_cat = request.form["form_color_hex"]
        print(name_cat)
        conn = db.get_db_connection()
        conn.execute("INSERT INTO categories (category, color, description) VALUES (?,?,?)",
                     (name_cat, color_cat, desc_cat,))
        conn.commit()
        conn.close()
    return "done"


@app.route('/app/categories/edit/<string:id>', methods=["GET", "POST"])
def categories_edit(id):
    if request.method == "POST":
        name_cat = request.form["form_name_category"]
        desc_cat = request.form["form_desc_category"]
        color_cat = request.form["form_color_hex"]
        print(name_cat)
        conn = db.get_db_connection()
        conn.execute("UPDATE categories SET category = ?, color = ?, description = ? WHERE id = ?",
                     (name_cat, color_cat, desc_cat, id,))
        conn.commit()
        conn.close()
    return "done"


@app.route('/app/categories/remove/<string:id>', methods=["GET", "POST"])
def categories_remove(id):
    if request.method == "POST":
        conn = db.get_db_connection()
        conn.execute("DELETE FROM categories WHERE id = ?", (id,))
        conn.execute("DELETE FROM categories_records WHERE category_id = ?", (id,))
        conn.commit()
        conn.close()
    return "done"


@app.route('/app/categories/update')
def categories_overview_update():
    conn = db.get_db_connection()
    categorie = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template('customElements/categories_list.html', categories=categorie)


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run()
