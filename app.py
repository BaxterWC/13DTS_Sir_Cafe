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


@app.route('/menu/<cat_id>')
def render_menu(cat_id):  # put application's code here
    con = connect_to_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products WHERE fk_cat_id=?"
    query_cat_list = "SELECT * FROM categories"
    cur = con.cursor()
    cur.execute(query, (cat_id,))
    product_list = cur.fetchall()
    cur.execute(query_cat_list)
    cat_list = cur.fetchall()
    print(product_list)
    print(cat_list)
    con.close()
    return render_template('menu.html', list_of_coffees=product_list, list_of_categories=cat_list)


@app.route('/contact')
def render_contact():  # put application's code here
    return render_template('contact.html')


@app.route('/about')
def render_about():  # put application's code here
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
