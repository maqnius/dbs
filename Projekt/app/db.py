import psycopg2
from psycopg2.sql import SQL, Identifier
import sys
from appconfig import config
import models
import converts
from exceptions import error_stat
from helpsers import cached

"""
This is where the magic happens!

"""

# Connect to database
db = psycopg2.connect(**config['database'])


@cached
def distribution():
    return {"hi": "hi"}


@cached
def get_all():
    cur = db.cursor()

    # Get max and min amount of transaction
    cur.execute("SELECT MAX(satoshis), MIN(satoshis) FROM txoutput where satoshis > 0;")
    max_sat, min_sat = cur.fetchone()

    # Get all transactions
    query = """
    SELECT i.wallet, o.wallet, o.satoshis 
    FROM txinput as i, txoutput as o
    WHERE i.txid = o.txid AND
    i.wallet <> o.wallet AND
    o.satoshis > 0 AND 
    o.wallet in (select w.walletid from wallets as w) AND
    i.wallet in (select w.walletid from wallets as w);
    """
    # cur.execute(query)
    # print(cur.rowcount)

    query = """
    SELECT wallet, SUM(satoshis)
    from txoutput, wallets
    where wallet = walletid group by wallet;
    """

    cur.execute(query)
    print(cur.rowcount)
    print(cur.fetchmany(20))

    return {}


@cached
def test_graph():
    return {
        "nodes": [
            {
                "id": "n0",
            },
            {
                "id": "n1",
            },
            {
                "id": "n2",
            }
        ],
        "edges": [
            {
                "id": "e0",
                "source": "n0",
                "target": "n1"
            },
            {
                "id": "e1",
                "source": "n1",
                "target": "n2"
            },
            {
                "id": "e2",
                "source": "n2",
                "target": "n0"
            }
        ]
    }


def _create_tables():
    """
    Will create the actual relations from our temporary tables

    """
    cur = db.cursor()

    print('Creating table wallets..')
    cur.execute(models.WALLETS)
    db.commit()

    cur.close()


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
    print("Wrote {} entries into the database:".format(written))
    print(error_stat(errors))

    # For transaction_output.csv
    cur.execute(models.TXOUTPUT)
    db.commit()

    print("Filling txoutput table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXOUTPUT)
    print("Wrote {} entries into the database:".format(written))
    print(error_stat(errors))

    # For transaction_blocks.csv
    cur.execute(models.TXBLOCKS)
    db.commit()

    print("Filling txblocks table...")
    errors, written = converts.fill_table(db, **converts.CONF_TXBLOCKS)
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

    _drop_tables(['transactions', 'transfer', 'wallets', 'users'])
    _create_tables()
    db.close()
