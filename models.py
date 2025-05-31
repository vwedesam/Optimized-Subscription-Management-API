from core.extensions import db, flask_bcrypt
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    
class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Free, Basic, Pro
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now())
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def is_current(self):
        return self.is_active and self.end_date > datetime.now()

    def cancel(self):
        self.is_active = False
        self.end_date = datetime.now()

