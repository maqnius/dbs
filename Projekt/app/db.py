import psycopg2
from psycopg2.sql import SQL, Identifier
import sys
from appconfig import config
import models
import converts
from exceptions import error_stat
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
    db.commit()
    
    print("Filling txinput table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXINPUT)
    db.commit()
    print("Wrote {} entries into the database:".format(written))
    print(error_stat(errors))

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    db.commit()

    print("Filling txoutput table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXOUTPUT)
    db.commit()
    print("Wrote {} entries into the database:".format(written))
    print(error_stat(errors))

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    db.commit()

    print("Filling txblocks table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXBLOCKS)
    db.commit()
    print("Wrote {} entries into the database:".format(written))
    print(error_stat(errors))

    cur.close()


def _drop_tables(tables):
    """
    Drops given tables

    Parameters
    ----------
    tables: List
        List of table names

    """

    cur = db.cursor()

    for table in tables:
        cur.execute(SQL("DROP TABLE IF EXISTS {}").format(Identifier(table)))

    db.commit()
    cur.close()


if __name__ == '__main__':
    if "--scratch" in sys.argv:
        # Deletes grounding Database and builds up everything from scratch
        _drop_tables(["txinput", "txoutput", "txblocks"])
        _create_temporary_tables()

    _drop_tables(['txs', 'transfer', 'wallets', 'users'])
    _create_tables()
    db.close()

