from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DATABASE = 'cafe_fr'

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "secret_key"

def is_logged_in():
    if session.get('user_id') is None:
        print("Not logged in")
        return False
    else:
        print("logged in")
        return True

def connect_to_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error:
        print("an error has occurred connecting to the database")
    return


@app.route('/')
def render_home():  # put application's code here
    user_name = None

    if 'user_id' in session:
        con = connect_to_database(DATABASE)
        cur = con.cursor()
        query = "SELECT fname FROM user WHERE user_id = ?"
        cur.execute(query, (session['user_id'],))
        guy = cur.fetchone()
        con.close()

        if guy:
            user_name = guy[0]

    return render_template('home.html', user_name=user_name)


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


@app.route('/admin')
def render_admin():  # put application's code here
    return render_template('admin.html')


@app.route('/about')
def render_about():  # put application's code here
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login_page():
    if request.method == 'POST':
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')

        con = connect_to_database(DATABASE)
        if con:
            cur = con.cursor()
            query = "SELECT user_id, email, password, fname, role FROM user WHERE email = ?"
            cur.execute(query, (email,))
            user_info = cur.fetchone()
            con.close()

            if user_info:

                if bcrypt.check_password_hash(user_info[2], password):
                    session['user_id'] = user_info[0]
                    session['email'] = user_info[1]
                    session['fname'] = user_info[3]
                    session['role'] = user_info[4]
                    return redirect("/")

        return redirect("\login?error=invalid+credentials")

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def render_signup():  # put application's code here
    if request.method == 'POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')
        password2 = request.form.get('user_password2')
        role = request.form.get('user_role')

        if password != password2:
            return redirect("\signup?error=passwords+do+not+match")

        if len(password) < 8:
            return redirect("\signup?error=password+is+too+short")

        hashed_password = bcrypt.generate_password_hash(password)

        con = connect_to_database(DATABASE)
        quer_insert = "INSERT INTO user(fname, lname, email, password, role) VALUES (?, ?, ?, ?, ?)"
        cur = con.cursor()
        query1 = "SELECT email FROM user"
        cur.execute(query1)
        all_emails = cur.fetchall()
        if (email,) in all_emails:
            return redirect("\signup?error=email+already+in+use")
        cur.execute(quer_insert, (fname, lname, email, hashed_password, role))
        con.commit()
        con.close()

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/add_category', methods=['POST', 'GET'])
def add_category():
    if not is_logged_in():
        return redirect("/?message=not+logged+in")
    if request.method == 'POST':
        cat_name = request.form.get('cat_name')
        con = connect_to_database(DATABASE)
        query_insert = 'INSERT INTO categories (cat_name) VALUES (?)'
        cur = con.cursor()
        cur.execute(query_insert, (cat_name,))
        con.commit()
        con.close()
    return render_template('admin.html', logged_in=is_logged_in())


@app.route('/delete_category', methods=['POST', 'GET'])
def delete_category():
    if not is_logged_in():
        return redirect("/?message=not+logged+in")
    if request.method == 'POST':
        category = request.form.get('select_cat')
        print(category)

        category = category.strip('(')
        category = category.strip(')')
        category = category.split(', ')

        cat_id = category[0]
        cat_name = category[1]
        print(f"cat_id = {cat_id} and cat_name = {cat_name}")
        return render_template('delete_confirm.html', cat_id=cat_id, name=cat_name, type="category")
    return redirect("/admin", logged_in=is_logged_in())

@app.route('/delete_confirm/<cat_id>')
def delete_confirm(cat_id):
    if not is_logged_in():
        return redirect("/?message=not+logged+in")
    con = connect_to_database(DATABASE)
    print(f'deleting {cat_id} from categories table')

    query = 'DELETE FROM categories WHERE cat_id=?'
    cur = con.cursor()
    cur.execute(query, (cat_id,))
    con.commit()
    con.close()
    return redirect('/admin')


if __name__ == '__main__':
    app.run()
