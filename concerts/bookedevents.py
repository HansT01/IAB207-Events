from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

from .models import Event

bp = Blueprint("bookedevents", __name__, url_prefix="/bookedevents")


@bp.route("/", methods=["GET", "POST"])
@login_required
def show():
    """
    Renders the bookedevents page by quering bookings with the current user's id.
    Requires the user to be logged in.
    """
    bookings = current_user.bookings
    if bookings == []:
        flash("No bookings found")

    for booking in bookings:
        event = Event.query.get(booking.event_id)
        setattr(booking, "event", event)

        if event.tickets == 0 and event.status == "upcoming":
            setattr(event, "status_display", "booked")
        else:
            setattr(event, "status_display", event.status)

    return render_template(
        "pages/bookedevents.jinja",
        bookings=enumerate(bookings),
    )
