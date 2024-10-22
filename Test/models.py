from datetime import datetime
from Test import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    emails_rcvd = db.relationship('Email', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Email(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Text, nullable=False)
    from_addr = db.Column(db.String(120), nullable = False)
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    attachments = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Email('{self.date}', '{self.from_addr}', '{self.subject}', '{self.body}')"
