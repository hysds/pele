import datetime

from flask import current_app, g
from pele import db, bcrypt, login_manager
from pele.extensions import auth


def authenticate(cls, email, password):
    """Authenticate and return user."""

    user = User.query.filter_by(email=email.lower()).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return None
    if not user.verified:
        current_app.logger.debug(f"User {user.email} not verified.")
        return None
    return user


def verify(cls, email, verification_code):
    """Verify email address."""

    user = User.query.filter_by(email=email.lower()).first()
    if not user or not bcrypt.check_password_hash(user.verification_code,
                                                  verification_code):
        return None
    if user.verified: return user
    user.verified = True
    user.verified_on = datetime.datetime.now()
    db.session.commit()
    return user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    verified_on = db.Column(db.DateTime, nullable=True)
    verification_code = db.Column(db.String(255), nullable=False)

    def __init__(self, email=None, password=None, verification_code=None):
        self.email = email.lower()
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.verified = False
        self.verified_on = None
        self.verification_code = bcrypt.generate_password_hash(
            verification_code, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email').lower()
        password = kwargs.get('password')
        if not email or not password:
            return None
        return authenticate(cls, email, password)

    @classmethod
    def verify(cls, **kwargs):
        email = kwargs.get('email').lower()
        verification_code = kwargs.get('verification_code')
        if not email or not verification_code:
            return None
        return verify(cls, email, verification_code)

    def to_dict(self):
        return dict(id=self.id, email=self.email)


@auth.verify_password
def verify_password(email, password):
    """Return True if user is verified False otherwise."""

    user = authenticate(User, email, password)
    if user is None:
        return False
    g.user = user
    return True
