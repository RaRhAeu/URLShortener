from datetime import datetime

import base62  # noqa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import DateTime, Integer, Unicode

from urlshortener.database import db
from urlshortener.utils import generate_short_url


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(
        Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    _short_url = db.Column(
        "short_url",
        Unicode(15),
    )
    long_url = db.Column(Unicode(255), nullable=False)
    created = db.Column(DateTime, default=datetime.utcnow)
    expires_at = db.Column(DateTime, nullable=True)
    visits = db.Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Url {self.id}: {self.short_url}>" # noqa

    @hybrid_property
    def short_url(self):
        return self._short_url

    @short_url.setter
    def short_url(self, short_url=None):
        if short_url:
            self._short_url = short_url
        else:
            self._short_url = generate_short_url(self.long_url)


# this should be hashed index, because we're not interested
# in BETWEEN like lookups, but only for a specific url
db.Index("urls_short_url_idx", Url._short_url, unique=True) # noqa
