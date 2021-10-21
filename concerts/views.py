from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import os

from .forms import (
    BookingForm,
    EventForm,
    FilterForm,
    LoginForm,
    RegisterForm,
    CommentForm,
)
from .models import Event, Comment, Booking, User
from . import db, app

mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    return render_template("pages/home.jinja")


@mainbp.route("/findevents", methods=["GET", "POST"])
def findevents():
    events = Event.query.all()

    for event in events:
        for comment in event.comments:
            username = User.query.filter_by(id=comment.user_id).first().username
            setattr(comment, "username", username)

    commentform = CommentForm()
    bookingform = BookingForm()
    filterform = FilterForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("bookedevents"))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
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


@mainbp.route("/myevents", methods=["GET", "POST"])
def myevents():
    events = Event.query.all()

    for event in events:
        for comment in event.comments:
            username = User.query.filter_by(id=comment.user_id).first().username
            setattr(comment, "username", username)
        setattr(event, "timestampformatted", event.timestamp.strftime("%Y-%m-%dT%H:%M"))
        print(event.desc)

    eventform = EventForm()
    commentform = CommentForm()
    bookingform = BookingForm()

    if eventform.validate_on_submit():
        event = Event.query.filter_by(id=eventform.event_id.data).first()
        if event:
            update_event(eventform)
        else:
            add_event(eventform)
        return redirect(url_for("main.myevents"))

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("main.myevents"))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        return redirect(url_for("main.myevents"))

    return render_template(
        "pages/myevents.jinja",
        events=enumerate(events),
        eventform=eventform,
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/bookedevents", methods=["GET", "POST"])
def bookedevents():
    bookings = Booking.query.all()

    # Attach username comments to events, attach events to bookings
    for booking in bookings:
        event = Event.query.filter_by(id=booking.event_id).first()
        for comment in event.comments:
            username = User.query.filter_by(id=comment.user_id).first().username
            setattr(comment, "username", username)
        setattr(booking, "event", event)

    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("main.bookedevents"))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        return redirect(url_for("main.bookedevents"))

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

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = "Incorrect email"
        elif not check_password_hash(user.hash, password):
            error = "Incorrect password"

        if error is None:
            login_user(user)
            return redirect(url_for("main.account"))
        else:
            flash(error)

        print("Successfully logged in")
        return redirect(url_for("main.account"))

    return render_template("pages/account.jinja", loginform=loginform)


@mainbp.route("/register", methods=["GET", "POST"])
def register():
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            print("Username already exists")
            return redirect(url_for("main.account"))

        hash = generate_password_hash(password)
        user = User(username=username, email=email, hash=hash)

        db.session.add(user)
        db.session.commit()

        flash("Successfully registered")
        return redirect(url_for("main.account"))

    return render_template("pages/register.jinja", registerform=registerform)


@mainbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.account"))


def check_upload_file(eventform):
    file = eventform.image.data
    filename = secure_filename(file.filename)
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(BASE_PATH, "static/images", filename)
    file.save(filepath)

    db_upload_path = "/static/images/" + filename
    return db_upload_path


def add_event(eventform):
    image = check_upload_file(eventform)
    timestamp = datetime.strptime(eventform.timestamp.data, "%Y-%m-%dT%H:%M")

    event = Event(
        timestamp=timestamp,
        title=eventform.title.data,
        artist=eventform.artist.data,
        genre=eventform.genre.data,
        venue=eventform.venue.data,
        status=eventform.status.data,
        desc=eventform.desc.data,
        tickets=eventform.tickets.data,
        price=eventform.price.data,
        image=image,
        user_id=current_user.id,
    )

    db.session.add(event)
    db.session.commit()


def update_event(eventform):
    event = Event.query.filter_by(id=eventform.event_id.data).first()

    image = check_upload_file(eventform)
    timestamp = datetime.strptime(eventform.timestamp.data, "%Y-%m-%dT%H:%M")

    event.timestamp = timestamp
    event.title = eventform.title.data
    event.artist = eventform.artist.data
    event.genre = eventform.genre.data
    event.venue = eventform.venue.data
    event.status = eventform.status.data
    event.desc = eventform.desc.data
    event.tickets = eventform.tickets.data
    event.price = eventform.price.data
    event.image = image
    event.user_id = current_user.id

    db.session.commit()


def add_comment(commentform):
    event_id = commentform.event_id.data
    comment = Comment(
        desc=commentform.desc.data,
        event_id=event_id,
        user_id=current_user.id,
    )

    db.session.add(comment)
    db.session.commit()


def add_booking(bookingform):
    tickets = bookingform.tickets.data
    price = bookingform.price.data
    event_id = bookingform.event_id.data

    booking = Booking(
        tickets=tickets, price=price, event_id=event_id, user_id=current_user.id
    )

    db.session.add(booking)
    db.session.commit()
