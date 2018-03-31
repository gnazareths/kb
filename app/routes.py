from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user_tasks = Task.query.filter_by(user_id=current_user.id)
    todo = [i for i in user_tasks if i.status == 1]
    doing = [i for i in user_tasks if i.status == 2]
    done = [i for i in user_tasks if i.status == 3]
    todo_form, doing_form, done_form = TaskForm(), TaskForm(), TaskForm()
    if todo_form.validate_on_submit():
        task = Task(name=todo_form.name.data, description=todo_form.description.data,
                    status=1, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Yay new challenge!')
        return redirect(url_for('index'))
    if doing_form.validate_on_submit():
        task = Task(name=doing_form.name.data, description=doing_form.description.data,
                    status=2, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Yay good luck!')
        return redirect(url_for('index'))
    if done_form.validate_on_submit():
        task = Task(name=done_form.name.data, description=done_form.description.data,
                    status=3, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Yay you did it!')
        return redirect(url_for('index'))
    return render_template('index.html', all=user_tasks, todo_form=todo_form,
        doing_form=doing_form, done_form=done_form, todo=todo, doing=doing,
        done=done)  ## can define vars here

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email and password combination')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
