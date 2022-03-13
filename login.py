from flask import Blueprint, render_template, redirect, url_for, request
from . import db #used database but will implement something more sophisticated for next assignment
#hardcoding the values, no db for this assignment

#password = "abd123"
#username = "mariam"

import unittest
#python -m unittest login.py

#validating using db
class loginuser(db.Model):
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


@app.route("/login", methods = ["GET", "POST"])
  def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    error = None
    if request.method == 'POST':
        if request.form['username'] != username or request.form['password'] !=                password:
            error = 'Invalid Login'
        else:
            return redirect(url_for('index2.html'))
    return render_template('index1.html', error=error)
