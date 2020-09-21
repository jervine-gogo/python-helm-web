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
    version = SelectField('remember me') # Added if/when I want to add additional helm version options
    records = SelectField('records', choices=[('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('100', '100'), ('150', '150'), ('200', '200'), ('256 (max)', '256')])
    submitButton = SubmitField("Submit")
