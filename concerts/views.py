from flask import Blueprint, render_template, redirect, url_for

from .forms import EventForm, LoginForm, RegisterForm
from .models import Event, Comment, Booking

mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    return render_template("pages/home.jinja")


@mainbp.route("/findevents")
def findevents():
    events = [sample_event(), sample_event()]
    return render_template("pages/findevents.jinja", events=enumerate(events))


@mainbp.route("/myevents")
def myevents():
    events = [sample_event(), sample_event()]
    form = EventForm()
    if form.validate_on_submit():
        print("Successfully saved event")
        return redirect(url_for("myevents"))
    return render_template("pages/myevents.jinja", events=enumerate(events), form=form)


@mainbp.route("/bookedevents")
def bookedevents():
    bookings = [sample_booking(), sample_booking()]
    return render_template("pages/bookedevents.jinja", bookings=enumerate(bookings))


@mainbp.route("/account")
def account():
    form = LoginForm()
    if form.validate_on_submit():
        print("Successfully logged in")
        return redirect(url_for("account"))
    return render_template("pages/account.jinja", form=form)


@mainbp.route("/register")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Successfully registered")
        return redirect(url_for("account"))
    return render_template("pages/register.jinja", form=form)


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
