from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database Setup

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS home(
id INTEGER PRIMARY KEY AUTOINCREMENT,
owner TEXT,
address TEXT,
members INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS donation(
id INTEGER PRIMARY KEY AUTOINCREMENT,
donor_name TEXT,
amount INTEGER
)
""")

conn.commit()
conn.close()

# Home

@app.route('/')
def home():
    return render_template("home.html")

# Register

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")

        conn.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name,email,password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# Login

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        ).fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')

    return render_template("login.html")

# Dashboard

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# NGO

@app.route('/ngo')
def ngo():
    return render_template("ngo.html")

# Add Home

@app.route('/addhome', methods=['GET','POST'])
def addhome():

    if request.method == "POST":

        owner = request.form['owner']
        address = request.form['address']
        members = request.form['members']

        conn = sqlite3.connect("users.db")

        conn.execute(
            "INSERT INTO home(owner,address,members) VALUES(?,?,?)",
            (owner,address,members)
        )

        conn.commit()
        conn.close()

        return redirect('/viewhome')

    return render_template("add_home.html")

# View Home

@app.route('/viewhome')
def viewhome():

    conn = sqlite3.connect("users.db")

    homes = conn.execute(
        "SELECT * FROM home"
    ).fetchall()

    conn.close()

    return render_template(
        "view_home.html",
        homes=homes
    )

# Edit Home

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    conn = sqlite3.connect("users.db")

    if request.method == "POST":

        owner = request.form['owner']
        address = request.form['address']
        members = request.form['members']

        conn.execute(
            "UPDATE home SET owner=?,address=?,members=? WHERE id=?",
            (owner,address,members,id)
        )

        conn.commit()
        conn.close()

        return redirect('/viewhome')

    home = conn.execute(
        "SELECT * FROM home WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_home.html",
        home=home
    )

# Delete Home

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("users.db")

    conn.execute(
        "DELETE FROM home WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/viewhome')

# Donation

@app.route('/donation', methods=['GET','POST'])
def donation():

    if request.method == "POST":

        donor_name = request.form['donor_name']
        amount = request.form['amount']

        conn = sqlite3.connect("users.db")

        conn.execute(
            "INSERT INTO donation(donor_name,amount) VALUES(?,?)",
            (donor_name,amount)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("users.db")

    donations = conn.execute(
        "SELECT * FROM donation"
    ).fetchall()

    conn.close()

    return render_template(
        "donation.html",
        donations=donations
    )


@app.route('/project')
def project():
    return render_template('project.html')
# Logout

@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)