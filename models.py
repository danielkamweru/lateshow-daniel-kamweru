from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from . import  db
class Episode(db.Model, SelializerMixin):
    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship(
        "Apperance",
        back_populates = "episode",
        cascade ="all, delete-orphan"
    )
    serialize_rules = ("-appearances.episode",)
class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    id = db.Column(db.Interger, primary_key= True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    appearances = db.relationship(
        "Appearance",
        back_populates = "guest",
        cascade = "all, delete-orphan"
    )
    serialize_rules = ("-apperances.guest",)
class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"))

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    serialize_rules = (
        "-episode.appearances",
        "-guest.appearances",
    )

    @validates("rating")
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating