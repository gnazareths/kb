from app import db, login
import enum
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(50))
    tasks = db.relationship('Task',
        lazy='dynamic', backref="user")

    def __repr__(self):
        return '<{}; {}>'.format(self.name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class TaskStatus(enum.Enum):
    TODO = "To do"
    DOING = "Doing"
    DONE = "Done"

class TaskCategory(enum.Enum):
    WORK = "Work"
    SCHOOL = "School"
    PERSONAL = "Personal"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.Enum(TaskStatus))
    category = db.Column(db.Enum(TaskCategory))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Board: {}>'.format(self.name)
