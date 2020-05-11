from datetime import datetime
from hashlib import sha256
import base62

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
    user_id = db.Column(
        Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        # index=True
    )
    # TODO: implement short_url directly in schema
    _short_url = db.Column("short_url", Unicode(15), nullable=False)
    long_url = db.Column(Unicode(255), nullable=False)
    created = db.Column(DateTime, default=datetime.utcnow)
    expires_at = db.Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Url: {self.id}>"

    def generate_short_url(self, URL_LEN=7):
        hs = sha256(self.long_url.encode('utf-8').digest())
        short_url = base62.encodebytes(hs)[:URL_LEN]
        return short_url

    @hybrid_property
    def short_url(self):
        return self._short_url

    @short_url.setter
    def short_url(self, short_url=None):
        if short_url is not None:
            self._short_url = short_url
        else:
            self._short_url = self.generate_short_url()


db.Index("urls_short_url_idx", Url._short_url, unique=True)