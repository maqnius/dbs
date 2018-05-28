import psycopg2

"""
This is where the magic happens!

"""


def init_db(config, empty_db=False):

    # Connect to database
    db = psycopg2.connect(**config)

    if empty_db:
        # Create tables if no tables yet
        _create_db(db)

    return db


def _create_db(db):
    # Create tables
    # Fill with content
    _parse_files(db)


def _parse_files(db):
    pass