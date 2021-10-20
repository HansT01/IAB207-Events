from flask import Blueprint, render_template, redirect, url_for

from .forms import BookingForm, EventForm, LoginForm, RegisterForm, CommentForm
from .models import Event, Comment, Booking

mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    return render_template("pages/home.jinja")


@mainbp.route("/findevents")
def findevents():
    events = [sample_event(), sample_event()]
    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        print("Successfully created comment")
        return redirect(url_for("bookedevents"))

    if bookingform.validate_on_submit():
        print("Successfully created booking")
        return redirect(url_for("bookedevents"))

    return render_template(
        "pages/findevents.jinja",
        events=enumerate(events),
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/myevents")
def myevents():
    events = [sample_event(), sample_event()]
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
    bookings = [sample_booking(), sample_booking()]
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


@mainbp.route("/account")
def account():
    loginform = LoginForm()

    if loginform.validate_on_submit():
        print("Successfully logged in")
        return redirect(url_for("account"))

    return render_template("pages/account.jinja", loginform=loginform)


@mainbp.route("/register")
def register():
    registerform = RegisterForm()

    if registerform.validate_on_submit():
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
