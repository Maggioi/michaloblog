from app import app, db
from flask import render_template, flash, redirect, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from datetime import datetime, timezone
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {"author" : {"username" : "michcio"},
         "body" : "what a lovely day"},
         {"author" : {"username" : "olcia"},
          "body" : "xenia!!!"}
    ]
    return render_template("index.html", title="hołm", posts=posts)

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/user/<username>')
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {"author" : user, "body": "Bloody lovely"},
        {"author": user, "body": "hell yeah"}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@login_required
@app.route('/edit_profile', methods=["GET", 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes has been set')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)