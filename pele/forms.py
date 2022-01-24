from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators


class LoginForm(Form):
    username = StringField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.optional()])
