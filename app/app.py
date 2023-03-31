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
    conn.close()
    return render_template('board.html')


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
