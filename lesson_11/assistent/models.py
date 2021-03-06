from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from assistent import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Note', backref = 'author', lazy='dynamic')
    contacts = db.relationship('Contact', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default =datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Note {}>'.format(self.body)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birthday = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Contact name - {} phone: {}, email: {}, birthday: {}, address: {}>'\
            .format(self.name, self.phone, self.email, self.birthday, self.address)

    # phones = db.relationship('Phone', backref='contact', lazy='dynamic')


# class Phone(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     phone = db.Column(db.String(50))
#     user_id = db.Column(db.Integer, db.ForeignKey('author.id'))
