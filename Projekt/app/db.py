import psycopg2
from appconfig import config
import models
import converts
from helpsers import get_uniqe_name

"""
This is where the magic happens!

"""


# Connect to database
db = psycopg2.connect(**config['database'])


def _create_tables():
    """
    Will create the actual relations from our temporary tables

    """

    cur = db.cursor()
    cur.execute(models.TXS)
    cur.execute(models.TRANSFER)
    cur.execute(models.WALLETS)
    cur.execute(models.USERS)

    cur.close()
    db.commit()


def _create_temporary_tables():
    """
    Creates temporary tables from the given input files to later
    merge those tables into our actual database scheme


    """
    cur = db.cursor()

    # For transaction_input.csv
    cur.execute(models.TXINPUT)
    converts.fill_table(db, **converts.CONF_TXINPUT)

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    converts.fill_table(db, **converts.CONF_TXOUTPUT)

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    converts.fill_table(db, **converts.CONF_TXBLOCKS)

    cur.close()
    # Commit to make changes persistent
    db.commit()


if __name__ == '__main__':
    _create_temporary_tables()
    # _create_tables()
    db.close()

