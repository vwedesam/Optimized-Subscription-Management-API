from core.extensions import db, flask_bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Integer, nullable=False)
    subscriptions = db.relationship('Subscription', backref='users', lazy=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)
    

class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Free, Basic, Pro
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.Integer, nullable=False)
    subscriptions = db.relationship('Subscription', backref='plans', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    created_at = db.Column(db.Integer, nullable=False)

    # indexes for Subscription model
    __table_args__ = (
        db.Index("idx_user_id_is_active_end_date_created_at", "user_id", "is_active", "end_date", db.desc("created_at")),
        db.Index("idx_user_id_created_at_desc", "user_id", db.desc("created_at")),
    )

