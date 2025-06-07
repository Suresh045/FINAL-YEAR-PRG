# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo,Length, Regexp
from wtforms.validators import Length, Regexp

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class HouseForm(FlaskForm):
    owner_name = StringField("Owner Name", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    satellite_image = FileField("Satellite Image", validators=[DataRequired()])
    submit = SubmitField("Add House")



class HouseApprovalForm(FlaskForm):
    owner_name = StringField("Owner Name", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Phone number must be 10 digits")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    house_address = StringField("House Address", validators=[DataRequired()])
    submit = SubmitField("Submit Application")