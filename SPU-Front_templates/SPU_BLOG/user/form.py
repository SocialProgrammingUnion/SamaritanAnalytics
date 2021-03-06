from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
        validators.Required(),
        validators.length(min=4, max=32)
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.length(min=4, max=80),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [
        validators.Required(),
        validators.length(min=4, max=32)
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.length(min=4, max=80),
    ])
