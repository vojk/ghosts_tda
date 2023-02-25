import csv
import io
import os

from flask import Flask, render_template, request, redirect, url_for, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from dotenv import load_dotenv
import db
import secrets
import sorting

pre_proglangs = [{'progLangs': 'Java'}, {'progLangs': 'Python'}, {'progLangs': 'C'}, {'progLangs': 'Ruby'},
                 {'progLangs': 'JavaScript'}, {'progLangs': 'TypeScript'}, {'progLangs': 'Kotlin'}]
list_of_elements = ["id", "date", "time-spent", "programming-language", "rating", "description"]

proglangs = sorted(pre_proglangs, key=lambda x: x['progLangs'])

secret_key = "61c42d54bdc57fdb8fa03af867511dff"


class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)

load_dotenv()

db  # inicializuje databázi


@app.route('/test/t')
def test():
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    prom = str(smtp_username) + " " + str(smtp_password) + " verze 2"
    return prom


@app.route('/')
@app.route('/app/', methods=["GET", "POST"])
@login_required
def app_wind():
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    categorie = conn.execute("SELECT * FROM categories WHERE user_id = ?", (protected_id(),)).fetchall()
    conn.close()
    return render_template('records.html', texts=sorting.pre_sort(None, None, None, None,
                                                                  None, None, None, current_user.get_id()),
                           defs=proglangs,
                           programmers=programmers, categories=categorie, users=programmers,
                           user_perm=protected_user_perm())


@app.route('/sort/')
def sort():
    sort_field = request.args.get('sort_field')
    filter_rating = request.args.get('filter_rating')
    filter_formatted_date = request.args.get('filter_formatted_date')
    filter_programmingLangs = request.args.get('filter_programmingLangs')
    filter_time = request.args.get('filter_time')
    filter_programmer = request.args.get('filter_programmer')
    filter_categories = request.args.get('filter_categories')
    print("programator: " + str(filter_programmer))
    print(sort_field)

    return render_template('customElements/table_row.html',
                           texts=sorting.pre_sort(sort_field, filter_rating, filter_programmingLangs,
                                                  filter_formatted_date,
                                                  filter_time, filter_programmer, filter_categories,
                                                  current_user.get_id()))


@app.route("/add/", methods=('GET', 'POST'))  # přidání záznamu
@app.route('/app/add/', methods=('GET', 'POST'))
def create_record():
    if request.method == 'POST':
        date = request.form['formDate']
        minutes = request.form['formMinutes']
        rating = request.form['formRating']
        progLang = request.form['formProgLang_select']
        desc = request.form['formDesc']
        categories = request.form['categories_overall']

        categories = categories.split(",")

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
            cursor.execute(
                'INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, user_id) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (date, minutes, progLang, rating, desc, current_user.get_id(),))
            conn.commit()
            last_id = cursor.lastrowid
            for categ in categories:
                cursor.execute(
                    'INSERT INTO categories_records (category_id, record_id, user_id) '
                    'VALUES (?, ?, ?)', (categ, last_id, protected_id(),))
                conn.commit()
            conn.close()
            return redirect(url_for('app_wind'))
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    categorie = conn.execute("SELECT * FROM categories WHERE user_id = ?", (protected_id(),)).fetchall()
    conn.close()
    return render_template('createWind.html', defs=proglangs, programmers=programmers, categories=categorie,
                           selected_categories="")


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
        categories = request.form['categories_overall']

        categories = categories.split(",")

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
            conn.execute("DELETE FROM categories_records WHERE record_id = ?", (id,))
            conn.commit()
            for categ in categories:
                conn.execute(
                    'INSERT INTO categories_records (category_id, record_id, user_id) '
                    'VALUES (?, ?, ?)', (categ, id, protected_id(),))
                conn.commit()
            conn.close()
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    categorie = conn.execute("SELECT * FROM categories WHERE user_id = ?", (protected_id(),)).fetchall()
    categorie_selected = conn.execute("SELECT category_id FROM categories_records WHERE record_id = ?",
                                      (id,)).fetchall()
    categorie_selected_formatted = ",".join([str(singleCat[0]) for singleCat in categorie_selected])
    categorie_selected_formatted = categorie_selected_formatted.split(",")
    conn.close()
    return render_template('editWind.html', record=record, defs=proglangs, programmers=programmers,
                           categories=categorie, selected_categories=categorie_selected_formatted)


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
        conn.execute("DELETE FROM categories_records WHERE record_id = ?", (id,))
        conn.commit()
        conn.close()
    return render_template('removeWarn.html')


# ----- login/logout -----

@login_manager.user_loader
def load_user(user_id):
    print("users_load")
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user is None:
        return None
    user = User(id=user[0], username=user[1], email=user[2], password=user[3])
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('app_login'))


@app.route('/app/login/', methods=["POST", "GET"])
def app_login():
    # If user is already authenticated, redirect to the protected page
    if current_user.is_authenticated:
        return redirect(url_for('protected'))

    if request.method == "POST":
        username = request.form["user_username"]
        password = request.form["user_password"]
        conn = db.get_db_connection()
        user = conn.execute("""SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?""",
                            (username, username, password)).fetchone()
        if user is not None:
            user_obj = User(id=user[0], username=user[1], email=user[2], password=user[3])
            login_user(user_obj)
            return redirect(url_for('protected'))
        else:
            print("user is not valid")
            return render_template("login/login.html")
    return render_template("login/login.html")


@app.route('/app/logout')
def app_logout():
    logout_user()
    return redirect(url_for('app_login'))


@app.route('/protected/')
@login_required
def protected():
    user_id = current_user.get_id()
    return redirect(url_for('app_wind'))


@app.route('/protected/get_user_id/')
@login_required
def protected_id():
    return current_user.get_id()


@app.route('/protected/get_user_perm/')
@login_required
def protected_user_perm():
    conn = db.get_db_connection()
    record = conn.execute("""SELECT role FROM users WHERE id=?""", (current_user.get_id(),)).fetchall()
    conn.close()
    return str(record[0][0])


# -------------------------


# ------ users management ---------

@app.route('/user/add/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_add_user():
    if request.method == "POST":
        firstname = request.form['form_firstname']
        lastname = request.form['form_lastname']
        username = request.form['form_username']
        email = request.form['form_email']
        password = request.form['form_password']
        perm = request.form['form_perm']
        conn = db.get_db_connection()
        how_many_of_it_is_username = conn.execute("""SELECT COUNT(*) FROM users WHERE username = ?;""",
                                                  (username,)).fetchall()
        how_many_of_it_is_email = conn.execute("""SELECT COUNT(*) FROM users WHERE email = ?;""",
                                               (email,)).fetchall()
        if not int(how_many_of_it_is_username[0][0]) >= 1:
            if not int(how_many_of_it_is_email[0][0]) >= 1:
                conn.execute(
                    'INSERT INTO users (username, firstname, lastname, password, email, role) '
                    'VALUES (?,?,?,?,?,?)', (username, firstname, lastname, password, email, perm))
                conn.commit()
            else:
                return "1"
        else:
            return "1"
        conn.close()
        return "0"
    return render_template('createUserWind.html', username="")


@app.route('/user/<int:user_id>/edit/', methods=["GET", "POST"])  # funkce pro upravení uživatele
def app_edit_user(user_id):
    print("id uživatele: " + str(user_id))
    conn = db.get_db_connection()
    if request.method == "POST":
        firstname = request.form['form_firstname']
        lastname = request.form['form_lastname']
        username = request.form['form_username']
        email = request.form['form_email']
        password = request.form['form_password']
        perm = request.form['form_perm']
        old_duplicates = conn.execute("""SELECT username, email FROM users WHERE id = ?""", (user_id,)).fetchall()
        how_many_of_it_is_username = conn.execute(
            """SELECT COUNT(*) FROM users WHERE username = ? AND username <> ?;""",
            (username, old_duplicates[0][0],)).fetchall()
        how_many_of_it_is_email = conn.execute("""SELECT COUNT(*) FROM users WHERE email = ? AND email <> ?;""",
                                               (email, old_duplicates[0][1],)).fetchall()
        if not int(how_many_of_it_is_username[0][0]) >= 1:
            if not int(how_many_of_it_is_email[0][0]) >= 1:
                conn.execute(
                    'UPDATE users SET username = ?, firstname=?, lastname=?, email=?, password=?,role=? WHERE id = ?',
                    (username, firstname, lastname, email, password, perm, user_id,))
                conn.commit()
            else:
                return "E-mail se už používá"
        else:
            return "Uživatelské jméno se už používá"
    username = conn.execute("SELECT * FROM users WHERE id IS ?", (user_id,)).fetchall()
    conn.close()
    return render_template('createUserWind.html', username=username[0][1], firstname=username[0][2],
                           lastname=username[0][3], password=username[0][4], email=username[0][5], perm=username[0][6])


@app.route('/user/<string:username>/delete/', methods=["GET", "POST"])  # funkce pro vytvoření uživatele
def app_delete_user(username):
    if request.method == "POST":
        username = username
        conn = db.get_db_connection()
        programmer_id = db.get_id_of_user(username)
        conn.execute('DELETE FROM records WHERE user_id = ?', (programmer_id[0][0],))
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


# ------------------------------------------------


@app.route('/app/categories/')
def categories_overview():
    conn = db.get_db_connection()
    categorie = conn.execute("SELECT * FROM categories WHERE user_id=?", (protected_id())).fetchall()
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
        conn.execute("INSERT INTO categories (category, color, description, user_id) VALUES (?,?,?,?)",
                     (name_cat, color_cat, desc_cat, protected_id(),))
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
    categorie = conn.execute("SELECT * FROM categories WHERE user_id=?", (protected_id(),)).fetchall()
    conn.close()
    return render_template('customElements/categories_list.html', categories=categorie)


@app.route('/app/beta/filters')
def filters():
    conn = db.get_db_connection()
    programmers = conn.execute("SELECT * FROM users").fetchall()
    categorie = conn.execute("SELECT * FROM categories WHERE user_id=?", (protected_id(),)).fetchall()
    conn.close()
    return render_template('filters_wind.html', defs=proglangs, users=programmers, categories=categorie)


@app.route('/app/overview/<int:id>')
def overview(id):
    conn = db.get_db_connection()
    query = """
SELECT categories.category, categories.color
FROM categories
JOIN categories_records ON categories.id = categories_records.category_id
WHERE categories_records.record_id = ?
"""
    record = conn.execute("SELECT * FROM records WHERE id = ?", (id,)).fetchall()
    categories = conn.execute(query, (id,)).fetchall()
    categories_list_names = [category[0] for category in categories]
    categories_list_colors = [category[1] for category in categories]
    conn.close()
    return render_template('customElements/overallInfoAboutRecord.html', record=record, names=categories_list_names,
                           colors=categories_list_colors)


# ------ export/import csv ------

@app.route('/app/backup')
@login_required
def backup_main_screen():
    return render_template('_backup.html')


@app.route('/csv/export')
@login_required
def export_csv():
    csvlist = [["id", "datum", "cas", "jazyk", "hodnoceni", "poznamky"]]
    conn = db.get_db_connection()
    record = conn.execute(f"SELECT * FROM records WHERE user_id={protected_id()}").fetchall()
    conn.close()
    for recorde in record:
        list_lent = len(recorde) - 1
        templist = []
        for i in range(list_lent):
            templist.append(recorde[i])
            if i == 5:
                csvlist.append(templist)
                print(csvlist)
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(csvlist)
    output = si.getvalue()
    return jsonify({'csv_data': output})


@app.route('/csv/import', methods=["GET", "POST"])
@login_required
def import_csv():
    if request.method == "POST":
        conn = db.get_db_connection()
        cursor = conn.cursor()
        data = request.json
        csvlist = ["datum", "cas", "jazyk", "hodnoceni", "poznamky"]
        conn.execute("""DELETE FROM records WHERE user_id = ?""", (protected_id(),))
        conn.execute("""DELETE FROM categories_records WHERE user_id = ?""", (protected_id(),))
        conn.commit()
        for record in data:
            tmplist = []
            for element in csvlist:
                tmplist.append(record[element])
            cursor.execute(
                """INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, user_id) VALUES (?,?,?,?,?,?)""",
                (tmplist[0], tmplist[1], tmplist[2], tmplist[3], tmplist[4], protected_id(),))
            conn.commit()
            last_id = cursor.lastrowid
            cursor.execute(
                'INSERT INTO categories_records (category_id, record_id, user_id) '
                'VALUES (?, ?, ?)', ("", last_id, protected_id(),))
            conn.commit()
        conn.close()
    return "file"


# ---- API Handler -----
@app.route('/users/<int:userid>/records', methods=['GET'])
def api_get_user_records(userid):
    list_of_records = []
    conn = db.get_db_connection()
    records = conn.execute("""SELECT * FROM records WHERE user_id = ?""", (userid,)).fetchall()
    conn.close()
    for record in records:
        list_lent = len(record) - 1
        templist = {}
        for i in range(list_lent):
            templist[list_of_elements[i]] = record[i]
        list_of_records.append(templist)
    return jsonify(list_of_records)


@app.route('/users/<int:userid>/records/<int:record_id>', methods=['GET'])
def api_get_user_record(userid, record_id):
    dictionary = {}
    conn = db.get_db_connection()
    records = conn.execute("""SELECT * FROM records WHERE user_id = ? AND id = ?""", (userid, record_id,)).fetchall()
    conn.close()
    for record in records:
        if record[0] == record_id:
            list_lent = len(record) - 1
            dictionary = {}
            for i in range(list_lent):
                dictionary[list_of_elements[i]] = record[i]
    return jsonify(dictionary)


@app.route('/users/<int:userid>/records', methods=['POST'])
def api_crate_user_record(userid):
    data = request.get_json()
    date = data['date']
    time = data['time-spent']
    programmingLang = data['programming-language']
    rating = data['rating']
    description = data['description']
    if int(rating) > 5 or int(rating) < 0:
        error_message = {
            "code": 422,
            "message": "rating must be <= 5"
        }
        return jsonify(error_message), 422
    if len(programmingLang) > 30:
        error_message = {
            "code": 422,
            "message": "programming-language must be <= 30"
        }
        return jsonify(error_message), 422
    if date == "" or time == "" or programmingLang == "" or rating == "" or description == "":
        error_message = {
            "code": 422,
            "message": "some of element is missing"
        }
        return jsonify(error_message), 422
    found = False
    for item in proglangs:
        if item['progLangs'] == programmingLang:
            found = True
            break
    if not found:
        error_message = {
            "code": 422,
            "message": "programming-language is not in the predefined programming languages"
        }
        return jsonify(error_message), 422
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO records (dates, timeInMinutes, programmingLang, rating, description, user_id) 
                    VALUES (?,?,?,?,?,?)""", (date, time, programmingLang, rating, description, userid,))
    conn.commit()
    record_id = cursor.lastrowid
    records = cursor.execute("""SELECT * FROM records WHERE id=?""", (record_id,)).fetchall()
    cursor.execute("""INSERT INTO categories_records (category_id, record_id, user_id) VALUES (?,?,?)""",
                   ("", record_id, userid,))
    conn.commit()
    for record in records:
        list_lent = len(record) - 1
        dictionary = {}
        for i in range(list_lent):
            dictionary[list_of_elements[i]] = record[i]
    conn.close()
    return jsonify(dictionary)


@app.route('/users/<int:userid>/records/<int:record_id>', methods=['PUT'])
def api_update_user_record(userid, record_id):
    data = request.get_json()
    date = data['date']
    time = data['time-spent']
    programmingLang = data['programming-language']
    rating = data['rating']
    description = data['description']
    if int(rating) > 5 or int(rating) < 0:
        error_message = {
            "code": 422,
            "message": "rating must be <= 5"
        }
        return jsonify(error_message), 422
    if len(programmingLang) > 30:
        error_message = {
            "code": 422,
            "message": "programming-language must be <= 30"
        }
        return jsonify(error_message), 422
    if date == "" or time == "" or programmingLang == "" or rating == "" or description == "":
        error_message = {
            "code": 422,
            "message": "some of element is missing"
        }
        return jsonify(error_message), 422
    found = False
    for item in proglangs:
        if item['progLangs'] == programmingLang:
            found = True
            break
    if not found:
        error_message = {
            "code": 422,
            "message": "programming-language is not in the predefined programming languages"
        }
        return jsonify(error_message), 422
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE records SET dates = ?, timeInMinutes = ?, programmingLang = ?, rating = ?, description = ?, user_id = ? 
                        WHERE id = ?""",
                   (date, time, programmingLang, rating, description, userid, record_id,))
    conn.commit()
    records = cursor.execute("""SELECT * FROM records WHERE id=?""", (record_id,)).fetchall()
    for record in records:
        list_lent = len(record) - 1
        dictionary = {}
        for i in range(list_lent):
            dictionary[list_of_elements[i]] = record[i]
    conn.close()
    return jsonify(dictionary)


@app.route('/users/<int:userid>/records/<int:record_id>', methods=['DELETE'])
def api_delete_user_record(userid, record_id):
    conn = db.get_db_connection()
    record = conn.execute("""SELECT * FROM records WHERE user_id = ? AND id = ?""", (userid, record_id,)).fetchone()
    if record is None:
        return jsonify("Not Found")
    conn.execute("""DELETE FROM records WHERE user_id = ? AND id = ?""", (userid, record_id,))
    conn.execute("""DELETE FROM categories_records WHERE record_id = ? AND user_id = ?""", (record_id, userid,))
    conn.commit()
    conn.close()
    return jsonify("200 OK")


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
