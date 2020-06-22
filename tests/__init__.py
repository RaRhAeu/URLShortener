from urlshortener.database import db


"""
TODO write tests for:
 +/- models
 - schemas
 - routes
 - auth stuff
"""


def setup_db(app):
    """Method used to build a database"""
    db.app = app
    db.create_all()


def teardown_db():
    """Method used to destroy database"""
    db.session.remove()
    db.drop_all()
    # TODO: check docs on this one
    db.session.bind.dispose()


def clean_db():
    for table in db.metadata.sorted_tables:
        db.session.execute(table.delete())
