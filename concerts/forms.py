from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired("Enter an email")])
    password = PasswordField("Password", validators=[InputRequired("Enter a password")])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Enter a username")])
    email = StringField("Email", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired("Enter a password")])
    confirm = PasswordField(
        "Confirm password",
        validators=[
            InputRequired("Enter the password again"),
            EqualTo("confirm", message="Passwords should match"),
        ],
    )
    submit = SubmitField("Register")
