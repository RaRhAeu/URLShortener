import os
import struct
from datetime import datetime
from hashlib import sha256
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import (
    Integer,
    Unicode,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import INET

from urlshortener.database import db


class User(db.Model):
    """
    User model definition.
    """
    __tablename__ = "users"
    # __searchable_columns__ = ["name"]
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    email_address = db.Column(Unicode(255), nullable=False)
    first_name = db.Column(Unicode(255), nullable=False)
    last_name = db.Column(Unicode(255))
    urls = db.relationship('Url', backref='user')

    # Hashed password
    _password = db.Column("password", Unicode(128), nullable=False)

    # Time and IP of creation
    created = db.Column(DateTime, default=datetime.utcnow)
    created_ip = db.Column(INET)

    # Time and IP of the last login
    login_time = db.Column(DateTime)
    login_ip = db.Column(INET)

    # Password recovery information
    recover_key = db.Column(Integer)
    recover_time = db.Column(DateTime)
    recover_ip = db.Column(INET)

    # Other settings
    admin = db.Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User: {self.name}>"

    @classmethod
    def by_email_address(cls, email):
        """
        Return the user object whose email address is ``email``.
        """
        return cls.query(email_address=email).first()

    @classmethod
    def by_credentials(cls, email, password, *args, **kwargs):
        """
        Return the user object whose email is ``email``
        if the password is matching
        """
        user = cls.by_email_address(email)
        if user and user.validate_password(password):
            return user

    @classmethod
    def by_recover_key(cls, key):
        return cls.query(recover_key=key).first()

    @hybrid_property
    def name(self):
        if not self.last_name:
            return self.first_name

        return f"{self.first_name} {self.last_name}"

    def initials(self):
        parts = self.name.split()
        initials = [p[0].upper() for p in parts if len(p) > 2
                    and '.' not in p]
        return ''.join(initials)

    @hybrid_property
    def password(self):
        """Return the hashed version of the password"""
        return self._password

    @password.setter
    def password(self, password):
        """
        Hash ``password`` on the fly and store its hashed version
        """
        self._password = self._hash_password(password)

    @staticmethod
    def _hash_password(password, salt=None):
        if salt is None:
            salt = os.urandom(60)

        assert isinstance(password, str)
        assert isinstance(salt, bytes)

        salt_hash = sha256()
        salt_hash.update(salt)
        password_hash = sha256()
        password_hash.update(
            (password + salt_hash.hexdigest()).encode("utf-8")
        )

        return salt_hash.hexdigest() + password_hash.hexdigest()

    def validate_password(self, password):
        """
        Check password against existing credentials
        :param password: the password that was provided by the user to
            try abd authenticate. This is the clear text version that we
            will need to match against the hashed one in the database.
        :type password: str object.
        :return: Whether the password is valid
        :rtype: bool
        """
        assert isinstance(password, str)

        if not self.password or not password:
            return False

        password_hash = sha256()
        password_hash.update((password + self.password[:64]).encode("utf-8"))
        return self.password[64:] == password_hash.hexdigest()

    def generate_recover_key(self, ip):
        self.recover_key = struct.unpack("I", os.urandom(4))[0] & 0x7FFFFFFF
        self.recover_time = datetime.utcnow()
        self.recover_ip = ip
        return self.recover_key

    @hybrid_method
    def is_manager(self):
        return self.admin

    # PERMISSIONS
    def is_readable(self, user):
        """Does the current user have full read access?"""
        return self.is_writable(user)

    def is_writable(self, user):
        return user and (
            self.id == user.id or user.is_manager()
        )


db.Index(
    "users_lower_email_address_idx",
    db.func.lower(User.email_address),
    unique=True
)
