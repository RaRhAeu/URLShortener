from datetime import datetime


from sqlalchemy.types import (
    Integer,
    Unicode,
    DateTime,
)
from urlshortener.database import db


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(
        Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        # index=True
    )
    # user = db.relationship("User", innerjoin=True)
    # TODO: implement short_url directly in schema
    # _short_url = db.Column("short_url", Unicode(128), nullable=False)
    long_url = db.Column(Unicode(255), nullable=False)
    created = db.Column(DateTime, default=datetime.utcnow)
    expires_at = db.Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Url: {self.id}>"
