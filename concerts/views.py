from flask import Blueprint, render_template
from .models import Event, Comment

mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    return render_template("pages/home.html")


@mainbp.route("/findevents")
def findevents():
    events = [sample_event()]
    return render_template("pages/findevents.html", events=events)


def sample_event():
    title = "EVENT TITLE"
    artist = "ARTIST NAME"
    genre = "EVENT GENRE"
    datetime = "EVENT DATETIME"
    venue = "EVENT VENUE"
    desc = "EVENT DESCRIPTION"
    status = "EVENT STATUS"
    image = "EVENT IMAGE"
    tickets = 200
    price = 25

    event = Event(
        title, artist, genre, datetime, venue, desc, status, image, tickets, price
    )

    comment_user = "USERNAME"
    comment_desc = "COMMENT DESCRIPTION"
    comment_time = "3:19 AM"

    comment = Comment(comment_user, comment_desc, comment_time)
    event.add_comment(comment)

    return event
