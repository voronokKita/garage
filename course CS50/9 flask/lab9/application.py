"""
fall 2021 CS50 Lab 9: Birthdays
Web application which will keep track of friends’ birthdays.
"""
import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQL('sqlite:///birthdays.db')

BIRTHDAY_FORM = ["Name", "Month", "Day"]
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        """ Add the user's entry into the database. """

        # Get user's input;
        name = request.form.get('Name')
        month = request.form.get('Month')
        day = request.form.get('Day')

        # Check user's input for more-less correctness;
        error = False
        if len(name) == 0 or len(month) == 0 or len(day) == 0:
            flash("Fields must not be empty.")
            error = True
        else:
            try:
                month = int(month)
                day = int(day)
            except ValueError:
                flash("Month and day must be numbers.")
                error = True
            else:
                if month < 1 or month > 12:
                    flash("Month value incorrect.")
                    error = True
                elif day < 1 or day > DAYS_IN_MONTH[month - 1]:
                    flash("Day value incorrect.")
                    error = True

        if not error:
            """
            May assume that
            If the name and date are the same, then the user wants to delete this entry;
            If the name in the db, but the date is different, then the user wants to update the date.
            """
            result = db.execute('SELECT * FROM birthdays WHERE name == (?)', name)

            if len(result) == 0:
                db.execute('INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)', name, month, day)
            
            elif result[0]['month'] == month and result[0]['day'] == day:
                db.execute('DELETE FROM birthdays WHERE name == (?)', name)
            
            else:
                db.execute('UPDATE birthdays SET month = (?), day = (?) WHERE name = (?)', month, day, name)

        return redirect('/')

    else:
        """ Display the entries in the database on index.html. """
        friends = db.execute('SELECT name, month, day FROM birthdays')
        return render_template('index.html', form=BIRTHDAY_FORM, friends_list=friends)
