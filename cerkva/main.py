import sqlite3
from DATA import DATA
from flask import Flask, render_template, session, url_for, g, request,flash
import os

DATABASE = 'cerkva.db'
SECRET_KEY = ''
DEBAG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'cerkva.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('SQL_Cerkva.sql', 'r') as f:
        db.cursor().execute(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DATA(db)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', menu=dbase.get_menu())


@app.route('/poslugi')
def poslugi():
    return render_template('poslugi.html', menu=dbase.get_menu())


@app.route('/addprod', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        res = dbase.add_prod(request.form['product'], request.form['price'],request.form['image'])
    return render_template('addprod.html', menu=dbase.get_menu())


@app.route('/contact')
def contact():
    return render_template('contact.html', menu=dbase.get_menu())


@app.route('/register')
def register():
    return render_template('register.html', menu=dbase.get_menu())


@app.route('/buy')
def buy():
    return render_template('buy.html', menu=dbase.get_menu())


@app.route('/login')
def login():
    return render_template('login.html', menu=dbase.get_menu())


if __name__ == '__main__':
    app.run(debug=True)
