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
    """
    # For transaction_input.csv
    cur.execute(models.TXINPUT)
    db.commit()
    print("Filling txinput table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXINPUT)
    db.commit()
    print("Parsed {} Entries ({} Errors)".format(written + errors, errors))

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    db.commit()
    print("Filling txoutput table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXOUTPUT)
    db.commit()
    print("Parsed {} Entries ({} Errors)".format(written + errors, errors))
    """

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    db.commit()
    print("Filling txblocks table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXBLOCKS)
    db.commit()
    print("Parsed {} Entries ({} Errors)".format(written + errors, errors))

    cur.close()


def _drop_temporary_tables():
    """
    Drops temporary tables (temporary step only,
    if input code is finished this step will
    be dropped

    """
    cur = db.cursor()

    cur.execute("DROP TABLE if exists txinput;")
    cur.execute("DROP TABLE if exists txoutput;")
    cur.execute("DROP TABLE if exists txblocks;")

    db.commit()
    cur.close()

    cur.close()


if __name__ == '__main__':
    _drop_temporary_tables()
    _create_temporary_tables()

    # _create_tables()
    db.close()

