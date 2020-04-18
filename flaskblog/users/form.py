import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user

from flaskblog.models import User

password_validator = {
    "pattern": re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%¨&\*\(\)])(?=.{6,})"),
    "error_message": (
                "Password field must have at least 6 characters including at least" +
                " one digit, one lowercase letter, one capital letter, and one special character" +
                "(!, @, #, $, %, ¨, &)"
    )
}


class RegistrationForm(FlaskForm):

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
        if re.search(password_validator["pattern"], password.data) is None:
            raise ValidationError(password_validator["error_message"])


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


class UpdateAccountForm(FlaskForm):
    accepted_images_ext = ["jpg", "jpeg", "png", "bmp", "gif"]
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    file = FileField("Update Profile Picture", validators=[
        FileAllowed(
            accepted_images_ext,
            "We only accept images with the following file extensions: {}"\
                .format(', '.join(accepted_images_ext))
        )])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken. Please choose another one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken. Please choose another one.")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. Please register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password")])
    submit = SubmitField("Reset Password")

    def validate_password(self, password):
        if re.search(password_validator["pattern"], password.data) is None:
            raise ValidationError(password_validator["error_message"])
