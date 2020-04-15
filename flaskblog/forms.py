import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from flaskblog.models import User

class RegistrationForm(FlaskForm):
    email_pattern = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%¨&\*\(\)])(?=.{6,})")

    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        EqualTo("password")
    ])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken. Please choose another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken. Please choose another one.")

    def validate_password(self, password):
        if re.search(self.email_pattern, password.data) is None:
            raise ValidationError("Password field must have at least 6 characters including at least one digit, one lowercase letter, one capital letter, and one special character (!, @, #, $, %, ¨, &)")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
