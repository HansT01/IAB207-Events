class Event:
    def __init__(
        self, title, artist, genre, datetime, venue, desc, status, image, tickets, price
    ):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.datetime = datetime
        self.venue = venue
        self.desc = desc
        self.status = status
        self.image = image
        self.tickets = tickets
        self.price = price

        self.comments = list()

    def add_comment(self, comment):
        self.comments.append(comment)


class Comment:
    def __init__(self, user, desc, created_at):
        self.user = user
        self.desc = desc
        self.created_at = created_at

    def __repr__(self):
        str = ("User: {0}\n" "Description: {1}\n").format(self.user, self.desc)
        return str
