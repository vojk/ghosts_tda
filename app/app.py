import csv
import io
import multiprocessing

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

import db
import secrets

secret_key = "61c42d54bdc57fdb8fa03af867511dff"

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = secret_key

db  # inicializuje databázi


#  funcke která nám vyrendruje main html records, a vyplní nám základní záznamy do tabulky
#  nejdřív se napojíme na databázi a fetchneme si data z databáze
#  něco to udělá ale nevím co
@app.route('/')  # main app lokalizace
@app.route('/app/', methods=["GET", "POST"])
def app_wind():
    conn = db.get_db_connection()
    records = conn.execute("SELECT * FROM records").fetchall()
    conn.close()
    return render_template('board.html', records=records)


@app.route('/note/add', methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        text = request.form['form-text']
        podpis = request.form['form-podpis']
        datum = request.form['form-date']
        if len(text) <= 120:
            if len(podpis) <= 28:
                conn = db.get_db_connection()
                conn.execute("INSERT INTO records (text, podpis, datum) VALUES (?,?,?)", (text, podpis, datum,))
                conn.commit()
                conn.close()
            else:
                return 'maximální délka pro podpis je víc než 120'
        else:
            return 'maximální délka pro text je víc než 120'
    return render_template('note_add.html')


@app.route('/note/manage/<int:id>/edit/', methods=['GET', 'POST'])
def edit_note(id):
    id = id
    if request.method == "POST":
        text = request.form['form-text']
        podpis = request.form['form-podpis']
        datum = request.form['form-date']
        if len(text) <= 120:
            if len(podpis) <= 28:
                conn = db.get_db_connection()
                conn.execute('UPDATE records SET text = ?, podpis= ?, datum = ? WHERE id = ?', (text, podpis, datum, id,))
                conn.commit()
                conn.close()
                return "update.html"
            else:
                return 'maximální délka pro podpis je víc než 120'
        else:
            return 'maximální délka pro text je víc než 120'
    return "update.html"


@app.route('/note/manage/<int:id>/remove', methods=['GET', 'POST'])
def remove_note(id):
    id = id
    if request.method == "POST":
        conn = db.get_db_connection()
        conn.execute('DELETE FROM records WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    return "remove.html"


@app.route('/board/')
def board_def():
    conn = db.get_db_connection()
    records = conn.execute("SELECT * FROM records").fetchall()
    conn.close()
    return render_template('board_sep.html', records=records)


@app.route('/board/editnote/<int:id>')
def board_def_edit(id):
    id = id
    conn = db.get_db_connection()
    records = conn.execute(f"SELECT * FROM records WHERE id = {id}").fetchall()
    conn.close()
    return render_template('note_edit.html', records=records)


@app.route('/statistics')
def render_stats():
    return render_template("statistics.html")


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
