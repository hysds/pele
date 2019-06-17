from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import validators


class LoginForm(Form):
    username = TextField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.optional()])
