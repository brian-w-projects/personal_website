from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, TextAreaField, HiddenField


class ContactForm(FlaskForm):
    email = StringField('Email:', validators=[validators.DataRequired(), validators.Email()])
    name = StringField('Name: ')
    information = TextAreaField('Information: ')
    next = HiddenField('Next: ')
    submit = SubmitField('Send')
