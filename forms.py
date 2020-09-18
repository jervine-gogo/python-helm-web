import os
from app import app
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms.fields.html5 import DateField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap

class deploySelectForm(FlaskForm):
    tiller_ns = SelectField('tiller_ns', choices=[], coerce=str)
    namespace = SelectField('namespace', choices=[], coerce=str)
    chart = SelectField('chart', choices=[])
    version = SelectField('remember me')
    submitButton = SubmitField("Submit")
