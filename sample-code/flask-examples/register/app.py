from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    connection = sqlite3.connect("lecture.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM registrants")
    rows = crsr.fetchall()
    return render_template("index.html", rows=rows)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="You must provide a name.")
        email = request.form.get("email").lower()
        if not email:
            return render_template("apology.html", message="You must provide an email.")
        connection = sqlite3.connect("lecture.db")
        crsr = connection.cursor()
        crsr.execute(f"INSERT INTO registrants (name, email) VALUES ('{name}', '{email}')")
        connection.commit()
        connection.close()
        return redirect("/")

@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    if request.method == "GET":
        return render_template("unsubscribe.html")
    else:
        email = request.form.get("email").lower()
        if not email:
            return render_template("apology.html", message="You must provide an email.")
        connection = sqlite3.connect("lecture.db")
        crsr = connection.cursor()
        crsr.execute(f"SELECT email FROM registrants WHERE email='{email}'")
        selection = crsr.fetchall()
        if not selection:
            connection.close()
            return render_template("apology.html", message="The email entered was not found.")
        crsr.execute(f"DELETE FROM registrants WHERE email='{email}'")
        connection.commit()
        connection.close()
        return redirect("/")