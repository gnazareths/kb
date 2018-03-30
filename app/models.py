from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

boards = db.Table('boards',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
        primary_key=True),
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'),
        primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(50))
    boards = db.relationship('Board', secondary=boards,
        lazy='subquery', backref=db.backref('pages', lazy=True)
    )

    def __repr__(self):
        return '<{}; {}>'.format(self.name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Board: {}>'.format(self.name)
