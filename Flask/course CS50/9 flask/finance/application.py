"""
fall 2021 CS50 PSet 9: C$50 Finance
A website where users can “buy” and “sell” stocks.
"""
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import os
from cs50 import SQL
from collections import namedtuple
from datetime import datetime, timezone

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.filters['usd'] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQL('sqlite:///finance.db')

# db tables:
"""
CREATE TABLE users (
    id INTEGER,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00,
    PRIMARY KEY(id)
);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE holdings (
    id INTEGER NOT NULL PRIMARY KEY,
    userid INTEGER NOT NULL,
    share TEXT,
    number NUMERIC,
    FOREIGN KEY(userid) REFERENCES users(id)
);
CREATE TABLE history (
    id INTEGER NOT NULL PRIMARY KEY,
    userid INTEGER NOT NULL,
    share TEXT,
    number NUMERIC,
    price NUMERIC,
    date DATETIME,
    FOREIGN KEY(userid) REFERENCES users(id)
);
"""

# Set namedtuple for index.html
Holding = namedtuple('Holding', 'symbol name shares price total')

# Make sure API key is set
if not os.environ.get('API_KEY'):
    raise RuntimeError('API_KEY not set')


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/')
@login_required
def index():
    """Show portfolio of stocks"""
    output = []
    wealth = 0
    cash = 0

    # Check db for user holdings
    userid = session['user_id']
    holdings = db.execute('SELECT share, number FROM holdings WHERE userid == (?)', userid)

    # Display user's stocks symbols, company name, number of shares,
    # current price, and total value of shares:
    for asset in holdings:
        symbol = asset['share']
        quote = lookup(symbol)
        if not quote:
            # now that's funny
            continue

        company = quote['name']
        number = asset['number']
        price = quote['price']
        total_cost = number * price

        # User total wealth
        wealth += total_cost

        entrie = Holding(symbol, company, number, price, total_cost)
        output.append(entrie)

    # Cash and total wealth
    cash = db.execute('SELECT cash FROM users WHERE id == (?)', userid)
    cash = cash[0]['cash']
    wealth += cash

    return render_template('index.html', user_holdings=output, cash=cash, wealth=wealth), 200


@app.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    """Get stock quote."""

    # Display form to request stock quote;
    if request.method == 'GET':
        return render_template('quote.html')

    # Lookup the stock symbol and check quote
    quote = lookup(request.form.get('symbol'))
    if not quote:
        return apology("must provide correct company symbol", 400)

    return render_template('quoted.html', company=quote['name'], symbol=quote['symbol'], price=quote['price']), 200


@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    """Buy shares of stock"""

    # Display form to bay a stock;
    if request.method == 'GET':
        return render_template('buy.html')

    # Check number
    number = request.form.get('shares')
    try:
        number = int(number)
    except ValueError:
        return apology("incorrect number of shares", 400)
    if number <= 0:
        return apology("you cannot buy emptiness, you already have it, deep in your soul", 400)

    # Check symbol
    quote = lookup(request.form.get('symbol'))
    if not quote:
        return apology("invalid symbol", 400)
    symbol = quote['symbol']

    # Check user cash
    userid = session['user_id']
    cash = db.execute('SELECT cash FROM users WHERE id == (?)', userid)
    cash = cash[0]['cash']
    price = quote['price']
    cost = number * price
    if cash - cost <= 0:
        return apology(f"insufficient funds to by {number} {symbol}", 400)

    # Perform buy operation:
    cash -= cost
    db.execute('UPDATE users SET cash = (?) WHERE id == (?)', cash, userid)

    # Insert or update?
    result = db.execute('SELECT share FROM holdings WHERE userid == (?) AND share == (?)', userid, symbol)
    if len(result) != 1:
        db.execute('INSERT INTO holdings (userid, share, number) VALUES (?, ?, ?)', userid, symbol, number)
    else:
        db.execute('UPDATE holdings SET number = number + (?) WHERE userid == (?) AND share == (?)', number, userid, symbol)

    # Make note in history
    date = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M'))
    db.execute('INSERT INTO history (userid, share, number, price, date) VALUES (?, ?, ?, ?, ?)',
               userid, symbol, number, price, date)

    # Output to user.
    flash("Bought!")
    return redirect(url_for('index'), code=302)


@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    """Sell shares of stock"""

    # Fill list of user holdings
    holdings_list = []
    userid = session['user_id']
    user_holdings = db.execute('SELECT share FROM holdings WHERE userid == (?)', userid)
    for asset in user_holdings:
        holdings_list.append(asset['share'])

    # Display form to sell a stock;
    if request.method == 'GET':
        return render_template('sell.html', holdings=holdings_list)

    # Check user input:
    number = request.form.get('shares')
    try:
        number = int(number)
    except ValueError:
        return apology("incorrect number of shares", 400)
    if number <= 0:
        return apology("you cannot sell emptiness, it forever yours", 400)

    quote = lookup(request.form.get('symbol'))
    if not quote or quote['symbol'] not in holdings_list:
        return apology("incorrect share symbol", 400)
    symbol = quote['symbol']

    # Check number of shares in user's disposal
    user_shares = db.execute('SELECT number FROM holdings WHERE userid == (?) AND share == (?)', userid, symbol)
    user_shares = user_shares[0]['number']
    if user_shares - number < 0:
        return apology(f"you don't have so many shares of {symbol}", 400)

    # Sell submited number of shares:
    # Take's shares from user
    db.execute('UPDATE holdings SET number = number - (?) WHERE userid == (?) AND share == (?)', number, userid, symbol)

    # Update user's cash
    price = quote['price']
    shares_sum = number * price
    db.execute('UPDATE users SET cash = cash + (?) WHERE id == (?) ', shares_sum, userid)

    # Make note in history
    date = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M'))
    db.execute('INSERT INTO history (userid, share, number, price, date) VALUES (?, ?, ?, ?, ?)',
               userid, symbol, number * -1, price, date)

    # Clean db from zero values
    if user_shares - number == 0:
        db.execute('DELETE FROM holdings WHERE userid == (?) AND share == (?)', userid, symbol)

    # Output to user.
    flash("Sold!")
    return redirect(url_for('index'), code=302)


@app.route('/history')
@login_required
def history():
    """Show history of transactions"""

    userid = session['user_id']
    history = db.execute('SELECT share, number, price, date FROM history WHERE userid == (?) ORDER BY date DESC', userid)

    # Display history in a table.
    return render_template('history.html', user_history=history)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""

    # Display form;
    if request.method == 'GET':
        return render_template('register.html')

    # Check input
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return apology("must provide username, password and password confirmation", 400)
    elif password != request.form.get('confirmation'):
        return apology("passwords do not match", 400)

    # Check database for existsting username
    result = db.execute('SELECT id FROM users WHERE username == (?)', username)
    if len(result) != 0:
        return apology("username already exists", 400)

    # Hash pasword and insert user in users table
    db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', username, generate_password_hash(password))

    # Query database for user id and set session
    result = db.execute('SELECT id FROM users WHERE username == (?)', username)
    session['user_id'] = result[0]['id']

    # Redirect to homepage.
    flash(f"Hello, {username}!")
    return redirect(url_for('index'), code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Display form;
    if request.method == 'GET':
        return render_template('login.html')

    # Ensure username and password
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return apology("must provide username and password", 403)

    # Query database for user
    result = db.execute('SELECT id, hash FROM users WHERE username == (?)', username)

    # Ensure username exists and password is correct
    if len(result) < 1 or not check_password_hash(result[0]['hash'], password):
        return apology("invalid username and/or password", 403)

    # Remember user
    session['user_id'] = result[0]['id']

    # Redirect to homepage.
    flash(f"Hi, {username}!", 'info')
    return redirect(url_for('index'), code=302)


@app.route('/repassword', methods=['GET', 'POST'])
def repassword():
    """Allow user to change password"""

    # Display form;
    if request.method == 'GET':
        return render_template('repassword.html')

    # Check input
    password_old = request.form.get('password_old')
    password_new = request.form.get('password_new')
    if not password_old or not password_new:
        s = "Must provide old password, new password and password confirmation:"
        return render_template('repassword.html', error=s)
    elif password_new != request.form.get('confirmation'):
        s = "Passwords do not match."
        return render_template('repassword.html', error=s)

    # Check for old password hash
    userid = session['user_id']
    old_hash = db.execute('SELECT hash FROM users WHERE id == (?)', userid)
    if len(old_hash) < 1 or not check_password_hash(old_hash[0]['hash'], password_old):
        s = "Invalid old password."
        return render_template('repassword.html', error=s)

    # Replase hash
    db.execute('UPDATE users SET hash = (?) WHERE id == (?)', generate_password_hash(password_new), userid)

    # Output to user.
    flash("Password changed successfully!")
    return redirect(url_for('index'), code=302)


@app.route('/logout')
def logout():
    """Log user out"""
    # Forget any user_id and redirect user to login form
    session.clear()
    return redirect(url_for('index'), code=302)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
