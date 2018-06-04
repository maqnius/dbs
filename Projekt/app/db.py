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
    print("Filling txinput table...")
    converts.fill_table(db, **converts.CONF_TXINPUT)

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    print("Filling txoutput table...")
    converts.fill_table(db, **converts.CONF_TXOUTPUT)

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    print("Filling txblocks table...")
    converts.fill_table(db, **converts.CONF_TXBLOCKS)

    cur.close()
    # Commit to make changes persistent
    db.commit()

def _drop_temporary_tables():
    """
    Drops temporary tables (temporary step only,
    if input code is finished this step will
    be dropped

    """
    cur = db.cursor()

    cur.execute("DROP TABLE txinput;")
    cur.execute("DROP TABLE txoutput;")
    cur.execute("DROP TABLE txblocks;")

    db.commit()
    cur.close()

    cur.close()


if __name__ == '__main__':
    _drop_temporary_tables()
    _create_temporary_tables()
    # _create_tables()
    db.close()

