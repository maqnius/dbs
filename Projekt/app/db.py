import psycopg2


def init_db(config, create_tables=False):

    # Connect to database
    db = psycopg2.connect(**config)

    if create_tables:
        create_tables(db)

    return db


def create_tables(db):
    # Create tables
    # Fill with content
    _parse_files(db)


def _parse_files(db):
    pass