from flask import render_template, request, redirect, flash
from __main__ import app

@app.route("/")
@app.route("/login")
def login():
    return render_template('principal/login.html')

@app.route("/inicio")
def inicio():
    return render_template('principal/login.html')