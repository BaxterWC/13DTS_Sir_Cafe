from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DATABASE = 'cafe_fr'
app = Flask(__name__)


def connect_to_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error:
        print("an error has occurred connecting to the database")
    return


@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')


@app.route('/menu')
def render_menu():  # put application's code here
    con = connect_to_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products"
    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    print(product_list)
    con.close()
    return render_template('menu.html')


@app.route('/contact')
def render_contact():  # put application's code here
    return render_template('contact.html')


@app.route('/about')
def render_about():  # put application's code here
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
