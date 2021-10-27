from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
import os

from .forms import EventForm
from .models import Event
from . import db

bp = Blueprint("myevents", __name__, url_prefix="/myevents")


@bp.route("/", methods=["GET", "POST"])
@login_required
def show():
    """
    Renders the myevents page by quering events with the current user's id.
    Requires the user to be logged in.
    """
    events = current_user.events
    if events == []:
        flash("No events found")

    for event in events:
        setattr(event, "timestampformatted", event.timestamp.strftime("%Y-%m-%dT%H:%M"))

        if event.tickets == 0 and event.status == "upcoming":
            setattr(event, "status_display", "booked")
        else:
            setattr(event, "status_display", event.status)

    eventform = EventForm()

    if eventform.validate_on_submit():
        event = Event.query.get(eventform.event_id.data)
        if event:
            update_event(eventform)
        else:
            add_event(eventform)
        return redirect(url_for("myevents.show"))

    return render_template(
        "pages/myevents.jinja",
        events=enumerate(events),
        eventform=eventform,
    )


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
        venue_name=eventform.venue_name.data,
        venue_address=eventform.venue_address.data,
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
    event.venue_name = eventform.venue_name.data
    event.venue_address = eventform.venue_address.data
    event.status = eventform.status.data
    event.desc = eventform.desc.data
    event.tickets = eventform.tickets.data
    event.price = eventform.price.data
    event.image = image
    event.user_id = current_user.id

    db.session.commit()
