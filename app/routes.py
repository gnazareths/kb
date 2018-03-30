from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')

@app.route('/index')
def index():
    user = {'username': 'Gui'}
    return render_template('index.html')  ## can define vars here

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Lgin requested for email {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
