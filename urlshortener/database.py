from flask_sqlalchemy import SQLAlchemy

"""
def query(cls, **kwargs):
    q = db.session.query(cls)
    if kw:
        q = q.filter_by(**kw)
    return q


# not needed i guess...
def get(cls, **kw):
    return cls.query(**kw).first() or None



"""


def exists(cls, **kwargs):
    return cls.query(**kwargs).first() is not None


db = SQLAlchemy()

# db = SQLAlchemy(session_options=dict(expire_on_commit=False))
db.Model.exists = classmethod(exists)
