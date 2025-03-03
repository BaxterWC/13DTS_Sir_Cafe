from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DATABASE = 'cafe_db'
app = Flask(__name__)


def connect_to_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print("an error has occured connecting to the database")
    return
@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')

@app.route('/menu')
def render_menu():  # put application's code here
    connection = connect_to_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products"
    cur = connection.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    print(product_list)
    return render_template('menu.html')


if __name__ == '__main__':
    app.run()
