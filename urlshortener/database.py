from flask_sqlalchemy import SQLAlchemy


def query(cls, **kwargs):
    q = db.session.query(cls)
    if kwargs:
        q = q.filter_by(**kwargs)
    return q


def get(cls, id):
    return cls.query().get(id)


def exists(cls, **kwargs):
    return cls.query(**kwargs).first() is not None


db = SQLAlchemy()

# db = SQLAlchemy(session_options=dict(expire_on_commit=False))
db.Model.query = classmethod(query)
db.Model.get = classmethod(get)
db.Model.exists = classmethod(exists)
