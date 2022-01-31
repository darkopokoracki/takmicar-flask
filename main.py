from os import popen
from flask import Flask, render_template, request, session, url_for, redirect
from importlib_metadata import re
import mysql.connector

from takmicar import Takmicar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djashdw278hds'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'ispit2022'
)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return 'Hello World'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
            'register.html'
        )

    prijava = request.form['prijava']
    ime_prezime = request.form['ime_prezime']
    email = request.form['email']
    sifra = request.form['sifra']
    potvrda = request.form['potvrda']
    informatika = request.form['informatika']
    matematika = request.form['matematika']


    if informatika == "":
        return render_template(
            'register.html',
            informatika_error = 'Morate uneti poene za informatiku!'
        )

    if matematika == "":
        return render_template(
            'register.html',
            matematika_error = 'Morate uneti poene za matematiku!'
        )

    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM takmicar WHERE broj_prijave = ?"
    values = (prijava, )
    cursor.execute(sql, values)
    
    res = cursor.fetchone()

    if res != None:
        return render_template(
            'register.html',
            prijava_error = 'Ovaj nalog vec postoji!'
        )

    if ' ' not in ime_prezime:
        return render_template(
            'register.html',
            ime_prezime_error = 'Mora postojati razmak!'
        )

    if '@' not in email:
        return render_template(
            'register.html',
            email_error = 'Mora postojati @ u emailu'
        )

    if len(sifra) < 3:
        return render_template(
            'register.html',
            sifra_error = 'Sifra mora da ima najmanje 3 karaktera'
        )

    if sifra != potvrda:
        return render_template(
            'register.html',
            potvrda_error = 'Sifre se ne poklapaju'
        )

    informatika = int(informatika)
    matematika = int(matematika)

    if informatika < 0 or matematika > 100:
        return render_template(
            'register.html',
            informatika_error = 'Broj poena mora biti izmedju 0 i 100'
        )

    if matematika < 0 or matematika > 100:
        return render_template(
            'register.html',
            matematika_error = 'Broj poena mora biti izmedju 0 i 100'
        )

    cursor = mydb.cursor(prepared = True)
    sql = "INSERT INTO takmicar VALUES(null, ?, ?, ?, ?, ?, ?)"
    values = (prijava, ime_prezime, email, sifra, informatika, matematika)
    cursor.execute(sql, values)
    mydb.commit()

    return 'Uspesno ste se registrovali'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template(
            'login.html'
        )

    prijava = request.form['prijava']
    sifra = request.form['sifra']

    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM takmicar WHERE broj_prijave = ?"
    values = (prijava, )
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res == None:
        return render_template(
            'login.html',
            prijava_error = 'Nalog sa tom prijavom ne postoji!'
        )

    res = dekodiraj(res)

    if res[4] != sifra:
        return render_template(
            'login.html',
            sifra_error = 'Pogresna lozinka!'
        )

    session['prijava'] = prijava

    return 'Uspesno ste se logovali' 


@app.route('/logout')
def logout():
	if 'prijava' in session:
		session.pop('prijava')
		return redirect(url_for('login'))
	else:
		return redirect(url_for('show_all'))


def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data


@app.route('/show_all')
def show_all():
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM takmicar"
    cursor.execute(sql)

    res = cursor.fetchall()

    n = len(res)
    for i in range(n):
        res[i] = dekodiraj(res[i])

    objekti = []

    for t in res:
        id = t[0]
        prijava = t[1]
        ime_prezime = t[2]
        email = t[3]
        sifra = t[4]
        informatika = t[5]
        matematika = t[6]

        takmicar = Takmicar(id, prijava, ime_prezime, email, sifra, informatika, matematika)
        objekti.append(takmicar)

    return render_template(
        'show_all.html',
        takmicari = objekti
    )


@app.route('/delete/<prijava>', methods=['POST'])
def delete(prijava):
    cursor = mydb.cursor(prepared = True)
    sql = "DELETE FROM takmicar WHERE broj_prijave = ?"
    values = (prijava, )
    cursor.execute(sql, values)
    mydb.commit()

    return redirect(
        url_for('show_all')
    )


@app.route('/update/<prijava>', methods=['GET', 'POST'])
def update(prijava):
    
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM takmicar WHERE broj_prijave = ?"
    values = (prijava, )
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res == None:
        return 'Ne postoji takmicar sa tom prijavom'

    res = dekodiraj(res)

    id = res[0]
    broj_prijave = res[1]
    ime_prezime = res[2]
    email = res[3]
    sifra = res[4]
    informatika = res[5]
    matematika = res[6]

    takmicar = Takmicar(id, broj_prijave, ime_prezime, email, sifra, informatika, matematika)


    if request.method == 'GET':
        return render_template(
            'update.html',
            takmicar = takmicar
        )

    if request.method == 'POST':
        prijava = request.form['prijava']
        ime_prezime = request.form['ime_prezime']
        email = request.form['email']
        sifra = request.form['sifra']
        potvrda = request.form['potvrda']
        informatika = request.form['informatika']
        matematika = request.form['matematika']

        if informatika == "":
            return render_template(
                'update.html',
                informatika_error = 'Morate uneti poene za informatiku!',
                takmicar = takmicar
            )

        if matematika == "":
            return render_template(
                'update.html',
                matematika_error = 'Morate uneti poene za matematiku!',
                takmicar = takmicar
            )

        if ' ' not in ime_prezime:
            return render_template(
                'update.html',
                ime_prezime_error = 'Mora postojati razmak!',
                takmicar = takmicar
            )

        if '@' not in email:
            return render_template(
                'update.html',
                email_error = 'Mora postojati @ u emailu',
                takmicar = takmicar
            )

        if len(sifra) < 3:
            return render_template(
                'update.html',
                sifra_error = 'Sifra mora da ima najmanje 3 karaktera',
                takmicar = takmicar
            )

        if sifra != potvrda:
            return render_template(
                'update.html',
                potvrda_error = 'Sifre se ne poklapaju',
                takmicar = takmicar
            )

        cursor = mydb.cursor(prepared = True)
        sql = "UPDATE takmicar SET ime_prezime = ?, email = ?, sifra = ?, matematika = ?, programiranje = ? WHERE broj_prijave = ?"
        values = (ime_prezime, email, sifra, matematika, informatika, prijava)
        cursor.execute(sql, values)
        mydb.commit()

        return redirect(
            url_for('show_all')
        )

app.run(debug = True)