from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.types import (
    Integer,
    Unicode,
    DateTime,
)
from urlshortener.database import db


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_id = db.Colum(
        Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    # TODO: read about sqlalchemy relationships
    user = db.relationship("User", innerjoin=True)
    _short_url = db.Column("short_url", Unicode(128), nullable=False)
    long_url = db.Column(Unicode(255), nullable=False)
    created = db.Column(DateTime, default=datetime.utcnow)
    expires_at = db.Column(DateTime, nullable=True)

    @hybrid_property
    def short_url(self):
        return self._short_url

    # TODO: implement short url setter or move the logic to api
    @short_url.setter
    def short_url(self, short_url):
        self._short_url = short_url

    def __repr__(self):
        return f"<Url: {self.short_url}>"
