from flask import Flask, render_template, request
import db

app = Flask(__name__)

db  # inicializuje databázi


@app.route('/')
def hello_world():  # main code base
    posts = [{'title': 'Test', 'test': ''}]
    return render_template('main.html', posts=posts)


@app.route("/test", methods=["POST"])  # Určení cesty /test & nastavení metody POST
def getRatingToText():  # Získání dat z formuláře v HTML dokumentu main.html
    if request.method == "POST":  # Kontroluje zda-li je metoda POST
        ratingSlider = request.form["_ratingSlider"]  # uloží data z _ratingSlider
        nameTextInput = request.form["_nameOfElement"]  # uloží data z _nameOfElement
        # Používá se "name" z form-input
        return 'rating: ' + ratingSlider + ' name: ' + nameTextInput  # navrátí hodnoty z ratingSlider a nameTextInput


if __name__ == '__main__':
    app.run()
