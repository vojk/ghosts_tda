from flask import Flask, render_template, request, flash, redirect, url_for
import db

import sqlite3

app = Flask(__name__)

db  # inicializuje databázi


@app.route('/')
def index():  # main code base
    return render_template('main.html')


# Testovací funkce pro čtení z <form>
@app.route("/test", methods=["POST"])  # Určení cesty /test & nastavení metody POST
def get_rating_to_text():  # Získání dat z formuláře v HTML dokumentu main.html
    if request.method == "POST":  # Kontroluje zda-li je metoda POST
        ratingSlider = request.form["_ratingSlider"]  # uloží data z _ratingSlider
        nameTextInput = request.form["_nameOfElement"]  # uloží data z _nameOfElement
        # Používá se "name" z form-input
        return 'rating: ' + ratingSlider + ' name: ' + nameTextInput  # navrátí hodnoty z ratingSlider a nameTextInput


@app.route("/blank")
def blank_site():
    return render_template('blank.html', text=db.read_data_from_db('u_default'))


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
        elif not minutes:
            print("No minutes found")
        elif not progLang:
            print("No progLang found")
        elif not desc:
            print("No desc found")
        else:
            conn = db.get_db_connection()
            conn.execute(
                'INSERT INTO u_default (dates, timeInMinutes, programmingLang, rating, description) VALUES (?, ?, ?, ?, ?)',
                (date, minutes, progLang, rating, desc))
            conn.commit()
            conn.close()
            return redirect(url_for('blank_site'))

    proglangs = [{'progLangs': 'JAVA'}, {'progLangs': 'PYTHON'}, {'progLangs': 'C#'}]
    return render_template('createWind.html', defs=proglangs)


if __name__ == '__main__':
    app.run()
