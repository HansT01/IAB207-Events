from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.fields import DateTimeField, FloatField, IntegerField, SelectField
from wtforms.fields import FileField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange

IMAGE_FILE_FORMATS = {"png", "jpg", "jpeg"}
IMAGE_FILE_FORMATS_MSG = "Only supports file formats: {0}".format(
    ", ".join(map(str, IMAGE_FILE_FORMATS))
)

EVENT_STATUS = {"upcoming", "inactive", "booked", "cancelled"}


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired("Enter an email")])
    password = PasswordField("Password", validators=[InputRequired("Enter a password")])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Enter a username")])
    email = StringField("Email", validators=[Email("Enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired("Enter a password")])
    confirm = PasswordField(
        "Confirm password",
        validators=[
            InputRequired("Enter the password again"),
            EqualTo("password", message="Passwords should match"),
        ],
    )
    submit = SubmitField("Register")


class EventForm(FlaskForm):
    title = StringField("Event title", validators=[InputRequired("Enter a title")])
    artist = StringField(
        "Artist name", validators=[InputRequired("Enter the name of the artist")]
    )
    genre = StringField("Genre", validators=[InputRequired("Enter the event genre")])
    datetime = DateTimeField(
        "Date and time", validators=[InputRequired("Enter a title")]
    )
    venue = StringField(
        "Venue address", validators=[InputRequired("Enter the venue address")]
    )
    desc = TextAreaField(
        "Description", validators=[InputRequired("Enter a description")]
    )
    status = SelectField(
        "Status",
        choices=EVENT_STATUS,
        validators=[InputRequired("Select a status")],
    )
    image = FileField(
        "Image",
        validators=[
            InputRequired("Image cannot be empty"),
            FileAllowed(IMAGE_FILE_FORMATS, message=IMAGE_FILE_FORMATS_MSG),
        ],
    )
    tickets = IntegerField(
        "Available tickets",
        validators=[NumberRange(min=0, message="Enter a valid number of tickets")],
    )
    price = FloatField(
        "Ticket price", validators=[NumberRange(min=0, message="Enter a valid price")]
    )
    submit = SubmitField("Save changes")


class CommentForm(FlaskForm):
    desc = TextAreaField(
        "Write a comment", validators=[InputRequired("Write a comment")]
    )
    submit = SubmitField("Comment")


class BookingForm(FlaskForm):
    tickets = IntegerField(
        "Number of tickets",
        validators=[
            InputRequired("Enter the number of tickets to book"),
            NumberRange(min=0, message="Enter a valid number of tickets"),
        ],
    )
    submit = SubmitField("Confirm booking")
