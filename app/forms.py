from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from form_validators import password_length
from models import User, Task, TaskStatus, TaskCategory

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

## Validate password!

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is taken.')

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[])
    category = SelectField(choices=[("TaskCategory.Work", TaskCategory.WORK.value), ("TaskCategory.School", TaskCategory.SCHOOL.value), ("TaskCategory.Personal", TaskCategory.PERSONAL.value)])
    submit = SubmitField('Add task')

class TodoForm(TaskForm):
    status = TaskStatus.TODO.value

class DoingForm(TaskForm):
    status = TaskStatus.DOING.value

class DoneForm(TaskForm):
    status = TaskStatus.DONE.value
