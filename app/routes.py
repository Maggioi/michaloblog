from app import app
from flask import render_template, flash, redirect, url_for, flash, redirect
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="hołm")
@app.route('/pakiernia')
def pakiernia():
    return render_template('pakiernia.html')
@app.route('/ford')
def ford():
    return render_template("ford.html")
@app.route('/przyprawy')
def przyprawy():
    return render_template("przyprawy.html")
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} intended logging in, remember me = {form.remember_me.data}')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)