from flask import Blueprint, render_template, redirect, url_for

from .forms import (
    BookingForm,
    EventForm,
    FilterForm,
    LoginForm,
    RegisterForm,
    CommentForm,
)
from .models import Event, Comment, Booking, User
from . import db

mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    return render_template("pages/home.jinja")


@mainbp.route("/findevents")
def findevents():
    events = Event.query.all()

    commentform = CommentForm()
    bookingform = BookingForm()
    filterform = FilterForm()

    if commentform.validate_on_submit():
        print("Successfully created comment")
        return redirect(url_for("bookedevents"))

    if bookingform.validate_on_submit():
        print("Successfully created booking")
        return redirect(url_for("bookedevents"))

    if filterform.validate_on_submit():
        print("Successfully filtered events")
        return redirect(url_for("bookedevents"))

    return render_template(
        "pages/findevents.jinja",
        events=enumerate(events),
        commentform=commentform,
        bookingform=bookingform,
        filterform=filterform,
    )


@mainbp.route("/myevents")
def myevents():
    events = Event.query.all()

    eventform = EventForm()
    commentform = CommentForm()
    bookingform = BookingForm()

    if eventform.validate_on_submit():
        print("Successfully saved event")
        return redirect(url_for("myevents"))

    if commentform.validate_on_submit():
        print("Successfully created comment")
        return redirect(url_for("myevents"))

    if bookingform.validate_on_submit():
        print("Successfully created booking")
        return redirect(url_for("myevents"))

    return render_template(
        "pages/myevents.jinja",
        events=enumerate(events),
        eventform=eventform,
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/bookedevents")
def bookedevents():
    bookings = Booking.query.all()

    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        print("Successfully created comment")
        return redirect(url_for("bookedevents"))

    if bookingform.validate_on_submit():
        print("Successfully created booking")
        return redirect(url_for("bookedevents"))

    return render_template(
        "pages/bookedevents.jinja",
        bookings=enumerate(bookings),
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/account", methods=["GET", "POST"])
def account():
    loginform = LoginForm()
    error = None

    if loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data

        print("Successfully logged in")
        return redirect(url_for("account"))

    return render_template("pages/account.jinja", loginform=loginform)


@mainbp.route("/register", methods=["GET", "POST"])
def register():
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        print("Successfully registered")
        return redirect(url_for("account"))

    return render_template("pages/register.jinja", registerform=registerform)


def sample_event():
    title = "EVENT TITLE"
    artist = "ARTIST NAME"
    genre = "EVENT GENRE"
    datetime = "EVENT DATETIME"
    venue = "EVENT VENUE"
    desc = "EVENT DESCRIPTION"
    status = "EVENT STATUS"
    image = "../../static/images/pexels-wendy-wei-1540406.jpg"
    tickets = 200
    price = 25

    event = Event(
        title, artist, genre, datetime, venue, desc, status, image, tickets, price
    )

    comment_user = "USERNAME"
    comment_desc = "COMMENT DESCRIPTION"
    comment_datetime = "COMMENT DATETIME"

    comment = Comment(comment_user, comment_desc, comment_datetime)
    event.add_comment(comment)

    comment_user = "USERNAME"
    comment_desc = "COMMENT DESCRIPTION"
    comment_datetime = "COMMENT DATETIME"

    comment = Comment(comment_user, comment_desc, comment_datetime)
    event.add_comment(comment)

    return event


def sample_booking():
    event = sample_event()
    id = 19568335
    datetime = "DATETIME"
    tickets = 1
    price = event.price

    booking = Booking(event, id, datetime, tickets, price)

    return booking
