from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from .forms import BookingForm, FilterForm, CommentForm
from .models import Event, Comment, Booking
from . import db

bp = Blueprint("findevents", __name__, url_prefix="/findevents")


@bp.route("/", methods=["GET", "POST"])
def show():
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

    # Limit search result to 10
    events = query.order_by(Event.timestamp.asc()).limit(10).all()
    if events == []:
        flash("No events found")

    for event in events:
        if event.tickets == 0 and event.status == "upcoming":
            setattr(event, "status_display", "booked")
        else:
            setattr(event, "status_display", event.status)

    filterform = FilterForm()

    return render_template(
        "pages/findevents.jinja",
        events=enumerate(events),
        filterform=filterform,
    )


@bp.route("/<id>", methods=["GET", "POST"])
def details(id):
    """
    Renders the eventdetails page.
    """
    event = Event.query.get(id)

    if event.tickets == 0 and event.status == "upcoming":
        setattr(event, "status_display", "booked")
    else:
        setattr(event, "status_display", event.status)

    commentform = CommentForm()
    bookingform = BookingForm()

    if commentform.validate_on_submit():
        add_comment(commentform)
        return redirect(url_for("findevents.details", id=id))

    if bookingform.validate_on_submit():
        add_booking(bookingform)
        return redirect(url_for("findevents.details", id=id))

    return render_template(
        "pages/eventdetails.jinja",
        event=event,
        commentform=commentform,
        bookingform=bookingform,
    )


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
        username=current_user.username,
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
        error = "Booking denied: Exceeded number of tickets available"
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
