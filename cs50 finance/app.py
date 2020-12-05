import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        stocks = {}
        allTotals = 0
        symbolDict = db.execute("SELECT DISTINCT name FROM purchases WHERE id=:id", id=session["user_id"])
        symbols = [str(key['name']) for key in symbolDict]
        for symbol in symbols:
            stocks[symbol] = []
            quote = lookup(symbol)
            stocks[symbol].append(quote['name'])
            sharesDict = db.execute("SELECT shares FROM purchases WHERE id=:userid AND name=:name", userid=session["user_id"], name=symbol)
            sharesList = [int(key['shares']) for key in sharesDict]
            shares = 0
            for share in sharesList:
                shares += int(share)
            stocks[symbol].append(shares)
            stocks[symbol].append(usd(quote['price']))
            total = float(quote['price']) * float(shares)
            allTotals += total
            stocks[symbol].append(usd(total))
        cash = db.execute("SELECT cash FROM users where id=:userid", userid=session["user_id"])[0]['cash']
        balance = usd(cash + allTotals)
        return render_template("index.html", stocks=stocks, cash=usd(cash), balance=balance, dark=session['dark'])
    else:
        if session['dark'] == 'false':
            session['dark'] = 'true'
        else:
            session['dark'] = 'false'
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html", dark=session['dark'])
    else:
        if not request.form.get("symbol"):
            return apology("A stock symbol is required to purchase shares", 403)
        elif lookup(request.form.get("symbol")) == None:
            return apology("The provided stock symbol was not found", 403)
        else:
            try:
                shares = int(request.form.get("shares"))
            except:
                return apology("Shares should be a positive integer", 403)
            if shares <= 0:
                return apology("Shares should be a positive integer", 403)
            quote = lookup(request.form.get("symbol"))
            cash = float(db.execute("SELECT cash FROM users WHERE id=:userid", userid=session["user_id"])[0]["cash"])
            if cash < (shares*float(quote['price'])):
                return apology("Not enough cash to purchase shares", 403)
            db.execute("INSERT INTO purchases (id, name, price, shares) VALUES (:userid, :name, :price, :shares)", userid=session["user_id"], name=request.form.get("symbol").upper(), price=float(quote['price']), shares=shares)
            db.execute("UPDATE users SET cash=:newbalance WHERE id=:userid", newbalance=cash - (shares*quote['price']), userid=session["user_id"])
            return redirect("/")

@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT name, price, shares, time FROM purchases WHERE id=:userid", userid=session["user_id"])
    if len(transactions) == 0:
        return apology("No transaction history (yet)", 403)
    for transaction in transactions:
        transaction['price'] = usd(transaction['price'])
    return render_template("history.html", transactions=transactions, dark=session['dark'])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['dark'] = 'false'

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html", dark=session['dark'])
    else:
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Stock not found", 403)
        return render_template("quoted.html", symbol=quote['name'], price=usd(quote['price']), dark=session['dark'])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Registration requires a username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Registration requires a password", 403)
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords entered do not match", 403)
        # Check if user exists before registering.
        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            if len(rows) != 0:
                return apology("That username already exists", 403)
            else:
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=generate_password_hash(request.form.get("password")))
                return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        symbolsDict = db.execute("SELECT DISTINCT name FROM purchases WHERE id=:userid", userid=session["user_id"])
        symbols = [symbol['name'] for symbol in symbolsDict]
        return render_template("sell.html", symbols=symbols, dark=session['dark'])
    else:
        sharesToSell = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        sharesDict = db.execute("SELECT shares FROM purchases WHERE id=:userid AND name=:name", userid=session["user_id"], name=symbol)
        sharesList = [int(key['shares']) for key in sharesDict]
        sharesOnHand = 0
        for share in sharesList:
            sharesOnHand += int(share)
        if sharesToSell > sharesOnHand:
            return apology("You do not have enough shares", 403)
        else:
            shares = -abs(sharesToSell)
        db.execute("INSERT INTO purchases (id, name, price, shares) VALUES (:userid, :name, :price, :shares)", userid=session["user_id"], name=symbol.upper(), price=float(quote['price']), shares=shares)
        cash = float(db.execute("SELECT cash FROM users WHERE id=:userid", userid=session["user_id"])[0]["cash"])
        db.execute("UPDATE users SET cash=:newbalance WHERE id=:userid", newbalance=cash + (sharesToSell*quote['price']), userid=session["user_id"])
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)