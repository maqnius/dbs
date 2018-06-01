import psycopg2
from appconfig import config
import models
import converts

"""
This is where the magic happens!

"""


def init_db(config):
    # Connect to database
    db = psycopg2.connect(**config)

    return db


def _create_tables(db):
    """
    Will create the actual relations from our temporary tables

    Parameters
    ----------
    db: database connection

    """
    pass


def _create_temporary_tables(db):
    """
    Creates temporary tables from the given input files to later
    merge those tables into our actual database scheme

    Parameters
    ----------
    db: database connection

    """
    cur = db.cursor()

    # For transaction_input.csv
    cur.execute(models.TXINPUT)
    converts.fill_table(cur=cur, path=converts.get_file('transactions_input.csv'), **models.CONF_TXINPUT)

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    converts.fill_table(cur=cur, path=converts.get_file('transactions_output.csv'), **models.CONF_TXOUTPUT)

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    converts.fill_table(cur=cur, path=converts.get_file('transactions_blocks.csv'), **models.CONF_TXBLOCKS)

    # Commit to make changes persistent
    db.commit()


if __name__ == '__main__':
    db = init_db(config['database'])
    _create_temporary_tables(db)
    _create_tables(db)
    db.close()

