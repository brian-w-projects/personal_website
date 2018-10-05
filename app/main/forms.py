from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, TextAreaField


class ContactForm(FlaskForm):
    email = StringField('Email:', validators=[validators.DataRequired(), validators.Email()])
    name = StringField('Name: ')
    information = TextAreaField('Information: ')
    submit = SubmitField('Send')