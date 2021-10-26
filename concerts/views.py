from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
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
    """
    Renders the findevents page.
    Will use URL parameters to filter events.
    """
    query = Event.query

    for key in request.args.keys():
        if request.args[key] != "" and request.args[key] != "submit":
            if key == "title":
                title = "%" + request.args["title"] + "%"
                query = query.filter(Event.title.like(title))
            if key == "artist":
                artist = "%" + request.args["artist"] + "%"
                query = query.filter(Event.artist.like(artist))
            if key == "genre":
                genre = "%" + request.args["genre"] + "%"
                query = query.filter(Event.genre.like(genre))
            if key == "aftertimestamp":
                aftertimestamp = request.args["aftertimestamp"]
                query = query.filter(Event.timestamp >= aftertimestamp)
            if key == "beforetimestamp":
                beforetimestamp = request.args["beforetimestamp"]
                query = query.filter(Event.timestamp <= beforetimestamp)
            if key == "status":
                status = request.args["status"]
                query = query.filter(Event.status.like(status))

    events = query.all()
    if events == []:
        flash("No events found")

    # Comments only have the user's id stored, so the username must be queried.
    for event in events:
        for comment in event.comments:
            username = User.query.get(comment.user_id).username
            setattr(comment, "username", username)

    commentform = CommentForm()
    bookingform = BookingForm()
    filterform = FilterForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("main.findevents"))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        return redirect(url_for("main.findevents"))

    return render_template(
        "pages/findevents.jinja",
        events=enumerate(events),
        commentform=commentform,
        bookingform=bookingform,
        filterform=filterform,
    )


@mainbp.route("/findevents/<id>", methods=["GET", "POST"])
def eventdetails(id):
    """
    Renders the eventdetails page.
    Will use URL parameters to filter events.
    """
    event = Event.query.get(id)

    for comment in event.comments:
        username = User.query.get(comment.user_id).username
        setattr(comment, "username", username)

    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("main.eventdetails", id=id))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        return redirect(url_for("main.eventdetails", id=id))

    return render_template(
        "pages/eventdetails.jinja",
        event=event,
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/myevents", methods=["GET", "POST"])
@login_required
def myevents():
    """
    Renders the myevents page by quering events with the current user's id.
    Requires the user to be logged in.
    """
    events = current_user.events
    if events == []:
        flash("No events found")

    # Comments only have the user's id stored, so the username must be queried.
    # The timestamp for html's datetime-local and how it is stored in the database has different formatting.
    for event in events:
        for comment in event.comments:
            username = User.query.get(comment.user_id).username
            setattr(comment, "username", username)
        setattr(event, "timestampformatted", event.timestamp.strftime("%Y-%m-%dT%H:%M"))

    eventform = EventForm()
    commentform = CommentForm()
    bookingform = BookingForm()

    if eventform.validate_on_submit():
        event = Event.query.get(eventform.event_id.data)
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
@login_required
def bookedevents():
    """
    Renders the bookedevents page by quering bookings with the current user's id.
    Requires the user to be logged in.
    """
    bookings = current_user.bookings
    if bookings == []:
        flash("No bookings found")

    # Bookings only have the event's id stored, so the event must be queried.
    # Comments only have the user's id stored, so the username must be queried.
    for booking in bookings:
        event = Event.query.get(booking.event_id)
        setattr(booking, "event", event)
        for comment in event.comments:
            username = User.query.get(comment.user_id).username
            setattr(comment, "username", username)

    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("main.bookedevents"))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        # bookings.price = bookings.price * bookings.tickets
        # db.session.commit()
        return redirect(url_for("main.bookedevents"))

    return render_template(
        "pages/bookedevents.jinja",
        bookings=enumerate(bookings),
        commentform=commentform,
        bookingform=bookingform,
    )


@mainbp.route("/account", methods=["GET", "POST"])
def account():
    """
    Renders the login page.
    """
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

        return redirect(url_for("main.account"))

    return render_template("pages/account.jinja", loginform=loginform)


@mainbp.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders the register page.
    """
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data
        contact = registerform.contact.data
        address = registerform.address.data

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for("main.account"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for("main.account"))

        hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            hash=hash,
            contact_number=contact,
            address=address,
        )

        db.session.add(user)
        db.session.commit()

        flash("Successfully registered")
        return redirect(url_for("main.account"))

    return render_template("pages/register.jinja", registerform=registerform)


@mainbp.route("/logout")
@login_required
def logout():
    """
    Logs out the user and redirects to the account page.
    """
    logout_user()
    flash("Successfully logged out")
    return redirect(url_for("main.account"))


def check_upload_file(eventform):
    """
    Uploads a file from form to database and return its upload path.
    If there is no input file and the event already exists, return the existing event's image upload path.
    If there is no input file and no existing event, return the default image upload path.
    """
    file = eventform.image.data
    event_id = eventform.event_id.data

    if file:
        filename = secure_filename(file.filename)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(BASE_PATH, "static/images", filename)
        file.save(filepath)

        db_upload_path = "/static/images/" + filename
        return db_upload_path

    elif event_id:
        event = Event.query.get(event_id)
        db_upload_path = event.image
        return db_upload_path

    else:
        flash("No image found, using default image")
        db_upload_path = "/static/images/image-regular.png"
        return db_upload_path


@login_required
def add_event(eventform):
    """
    Adds an event to the database.
    """
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


@login_required
def update_event(eventform):
    """
    Updates an event on the database.
    Requires the user to be logged in.
    """
    event = Event.query.get(eventform.event_id.data)

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


@login_required
def add_comment(commentform):
    """
    Adds a comment to the database.
    Requires the user to be logged in.
    """
    event_id = commentform.event_id.data
    comment = Comment(
        desc=commentform.desc.data,
        event_id=event_id,
        user_id=current_user.id,
    )

    db.session.add(comment)
    db.session.commit()


@login_required
def add_booking(bookingform):
    """
    Adds a booking to the database.
    Requires the user to be logged in.
    """
    tickets = bookingform.tickets.data
    price = bookingform.price.data
    event_id = bookingform.event_id.data
    event = Event.query.get(event_id)
    if tickets > event.tickets:
        error = "Booking denied :Exceeded number of tickets available"
        flash(error)
    else:
        booking = Booking(
            tickets=tickets,
            price=price,
            event_id=event_id,
            user_id=current_user.id,
        )
        event.tickets = event.tickets - tickets
        db.session.add(booking)
        db.session.commit()
