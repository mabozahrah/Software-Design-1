from flask import Flask, render_template, request, redirect, url_for, session

import unittest
#python -m unittest login.py

@app.route("/profile", methods = ["GET", "POST"])
  def profile():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'username' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'zipcode' in request.form 
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode'] 
    elif not re.match(r'[A-Za-z0-9]+', username):
                error = "Invalid Username"
    return render_template("index1.html", error = error)
  return redirect(url_for('index.html'))
    
