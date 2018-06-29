import numpy
import sys
import psycopg2
from psycopg2.sql import SQL, Identifier
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

MINNECC = 0


@cached
def distribution():
    global MINNECC

    cur = db.cursor()

    # Get sum of received satoshis grouped by wallet id
    query = """
    SELECT o.satoshis
    from txoutput as o, txinput as i, wallets as w
    where o.wallet = w.walletid
     and o.txid = i.txid
     and o.wallet <> i.wallet
     order by satoshis DESC;
    """

    cur.execute(query)
    result = cur.fetchall()

    # Convert result to numpy array
    satoshis = numpy.array([res[0] for res in result], dtype=numpy.int64)

    # Calculate histogram
    hist, edges = numpy.histogram(satoshis, bins=10, normed=True)

    # Define
    data = {
        'x': ["{}-{}".format(numpy.format_float_scientific(edges[i], precision=6),
                             numpy.format_float_scientific(edges[i + 1], precision=6))
              for i in range(len(edges) - 1)],
        'y': hist.tolist()
    }

    MINNECC = int(_calc_useful_data(satoshis))

    return data


def _calc_useful_data(result, vol=0.90):
    """
    Sum up n biggest amounts of transactions until volume is at least
    90 % of the maximum

    Parameters
    ----------
    result
    vol

    Returns
    -------

    """
    total = result.sum()

    acc = 0
    for i, res in enumerate(result):
        acc += res
        if acc / total > vol:
            print('Lower bound for satoshi transaction of {} is enough to have {} % of transaction vol. '
                  'Use of {} % of items ({}).'
                  .format(res, int(vol*100), int(i/len(result)*100), i))
            return res


@cached
def get_range():
    """
    Get min max

    Returns
    -------

    """
    cur = db.cursor()

    # Get max and min amount of transaction
    cur.execute("SELECT MAX(satoshis), MIN(satoshis) FROM txoutput where satoshis > 0;")

    return cur.fetchone()


@cached
def get_all():
    cur = db.cursor()

    # Get all transactions
    query = """
    SELECT i.wallet, o.wallet, o.satoshis 
    FROM txinput as i, txoutput as o
    WHERE i.txid = o.txid AND
    i.wallet <> o.wallet AND
    o.satoshis > %s AND 
    o.wallet in (select w.walletid from wallets as w) AND
    i.wallet in (select w.walletid from wallets as w);
    """
    cur.execute(query, (MINNECC,))
    print(cur.rowcount)
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
