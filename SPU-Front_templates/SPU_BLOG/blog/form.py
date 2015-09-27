from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from blog.models import Category

class SetupForm(Form):
    name = StringField('Blog Name', [
    validators.Required(),
    validators.Length(max=80)
    ])
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

def categories():
    return Category.query

class PostForm(Form):
    image = FileField('image', validators= [
        FileAllowed(['jpg','png','gif'], 'Images only!')
    ])
    title = StringField('Title', [
            validators.Required(),
            validators.Length(max=80)
        ])
    body = TextAreaField('Content', validators=[validators.Required()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New Category')
