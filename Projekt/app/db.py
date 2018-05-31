import psycopg2
import os
import csv
from appconfig import config
from converts import convert_input_string, convert_output_string
"""
This is where the magic happens!

"""


def init_db(config):
    # Connect to database
    db = psycopg2.connect(**config)
    return db


def _get_file(name):
    """
    Returns the path to a source file. It looks up the DATA folder and
    adds a 'test_' at the beginning of the path if TEST_FILES is True.

    Parameters
    ----------
    name: str
        filename

    Returns
    -------
    path

    """
    TEST_FILES = True
    DATA = './data'

    name = 'test_' + name if TEST_FILES else name
    return os.path.join(DATA, name)


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
    cur.execute("CREATE TABLE txinput ("
            "txid varchar PRIMARY KEY, "
            "walletid varchar, "
            "walletsign varchar, "
            "timestamp bigint "
            ");")

    conf = {
        'cur': cur,
        'path': _get_file('transactions_input.csv'),
        'table': 'txinput',
        'col_names': ['txid', 'walletid', 'walletsign', 'timestamp'],
        'use_cols': (0, 1, 4),
        'skip_rows': 1,
        'convert': {
            '1': convert_input_string
        }
    }

    _fill_tables(**conf)

    # For transaction_output.csv
    cur.execute("CREATE TABLE txoutput ("
                "txid varchar PRIMARY KEY, "
                "satoshis bigint, "
                "walletid varchar, "
                "timestamp bigint "
                ");")

    conf = {
        'cur': cur,
        'path': _get_file('transactions_output.csv'),
        'table': 'txoutput',
        'col_names': ['txid', 'satoshis', 'walletid', 'timestamp'],
        'use_cols': (0, 1, 2, 4),
        'skip_rows': 1,
        'convert': {
            '2': convert_output_string
        }
    }

    _fill_tables(**conf)

    # For transaction_blocks.csv
    cur.execute("CREATE TABLE txblocks ("
                "txid varchar PRIMARY KEY, "
                "blockid varchar, "
                "timestamp bigint "
                ");")

    conf = {
        'cur': cur,
        'path': _get_file('transactions_blocks.csv'),
        'table': 'txblocks',
        'col_names': ['txid', 'blockid', 'timestamp'],
        'use_cols': (0, 1, 6),
        'skip_rows': 1
    }

    _fill_tables(**conf)

    # Commit to make changes persistent
    db.commit()


def _fill_tables(cur, path, table, col_names, skip_rows=0, use_cols=(), convert={}, fill_missing={}):
    """
    Fills table using a csv input file

    Parameters
    ----------
    cur: database cursor
        Cursor of current database connection
    path: path
        Path to source csv file
    table: str
        Name of the table to fill
    col_names: tuple or list
        Names of the columns in the database table
    skip_rows: int
        Number of leading rows to skip in csv file. Default is 0
    use_cols: tuple or list
        Which cols of the csv file to use. Default is all.
    convert: dict
        Dictionary with optional convert functions for each row
    fill_missing: dict
        Dictionary of missing values for given columns

    """
    execute_string = "INSERT INTO {} ({}) VALUES ({})".format(
            table,
            ','.join(col_names),
            ','.join(['%s']*len(col_names))
            )

    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row_ix, row in enumerate(reader):
            # Skip rows
            if row_ix < skip_rows:
                continue

            entries = []    # will be filled with values for the database table row
            for ix, column in enumerate(row):
                if not use_cols or ix in use_cols:  # Only use data if in use_cols or no use_cols given
                    column = column.strip()

                    missing = False if column else True
                    if not missing:
                        try:
                            converted = convert[str(ix)](column)    # Convert it convert function given

                            # If we get two values from one entry. Happens with input strings
                            if type(converted) in (list, tuple):
                                entries += converted
                            else:
                                entries.append(converted)
                        except KeyError:
                            entries.append(column)
                        except TypeError:
                            # Type does not fit to convert function
                            # Enter missing routine in the next step
                            missing = True
                    if missing:
                        try:
                            # Fill if for this column there is a fill value given
                            fill_missing[str(ix)]
                        except KeyError:
                            break   # skips this column

            # If you came until here, you can finally add the values to the table
            cur.execute(execute_string, tuple(entries))


if __name__ == '__main__':
    db = init_db(config['database'])
    _create_temporary_tables(db)
    _create_tables(db)
    db.close()

