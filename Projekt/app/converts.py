import sys
import os
import csv
from psycopg2 import IntegrityError, errorcodes
from datetime import datetime
import time
from exceptions import ParseException, reset_errs, ERRS


def convert_basestring(base_string):
    if 27 <= len(base_string) <= 34:
        return base_string
    else:
        raise ParseException(1)


def convert_timestamp(timestamp):
    if int(timestamp) > time.time():
        timestamp = timestamp[:-3]
        ERRS[str(2)] += 1

    try:
        date = datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        raise ParseException(2)

    return date.isoformat(sep=' ')


def convert_sha256(input):
    if len(input) != 64:
        raise ParseException(3)
    else:
        return input


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
    TEST_FILES = False
    DATA = './data'

    name = 'test_' + name if TEST_FILES else name
    return os.path.join(DATA, name)


def fill_table(db, path, table, col_names, skip_rows=0, use_cols=(), convert={}, fill_missing={}, autocommit=False):
    """
    Fills table using a csv input file

    Parameters
    ----------
    db: database connection
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
    reset_errs()

    cur = db.cursor()

    execute_string = "INSERT INTO {} ({}) VALUES ({})".format(
        table,
        ','.join(col_names),
        ','.join(['%s']*len(col_names))
    )

    written = 0

    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row_ix, row in enumerate(reader):
            # Skip rows
            if row_ix < skip_rows:
                continue

            try:
                entries = _parse_row(row, convert, fill_missing, use_cols)

                # If you came until here, you can finally add the values to the table
                cur.execute(execute_string, tuple(entries))
                db.commit()
                written += 1
            except ParseException as e:
                # Not all columns could be parsed
                ERRS[str(e.code)] += 1
            except IntegrityError as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    # Already entry in table
                    db.rollback()

                    # Delete duplicate and continue
                    cur.execute("DELETE FROM txblocks WHERE txid = %s;", (row[0],))
                    if autocommit:
                        db.commit()
                    ERRS[str(4)] += 1
                else:
                    raise

    if not autocommit:
        db.commit()

    return ERRS, written


def _parse_row(row, convert, fill_missing, use_cols):
    entries = []

    for ix, column in enumerate(row):
        if not use_cols or ix in use_cols:  # Only use data if in use_cols or no use_cols given
            column = column.strip()
            try:
                if column:
                    try:
                        converted = convert[str(ix)](column)    # Convert it convert function given

                        # If we get two values from one entry. Happens with input strings
                        if type(converted) in (list, tuple):
                            entries += converted
                        else:
                            entries.append(converted)
                    except KeyError:
                        # No converter defined
                        entries.append(column)
                else:
                    raise ParseException(0)

            except ParseException as e:
                if str(ix) in fill_missing:
                    # Fill if for this column there is a fill value given
                    entries += fill_missing[str(ix)]
                else:
                    raise

    return entries


CONF_TXBLOCKS = {
    'path': _get_file('transactions_blocks.csv'),
    'table': 'txblocks',
    'col_names': ['txid', 'blockid', 'timest'],
    'use_cols': (0, 1, 6),
    'skip_rows': 1,
    'convert': {
        '0': convert_sha256,
        '1': convert_sha256,
        '6': convert_timestamp
    },
    'autocommit': True
}


CONF_TXINPUT = {
    'path': _get_file('transactions_input.csv'),
    'table': 'txinput',
    'col_names': ['txid', 'wallet', 'timest'],
    'use_cols': (0, 3, 4),
    'skip_rows': 1,
    'convert': {
        '0': convert_sha256,
        '3': convert_basestring,
        '4': convert_timestamp
    }
}


CONF_TXOUTPUT = {
    'path': _get_file('transactions_output.csv'),
    'table': 'txoutput',
    'col_names': ['txid', 'satoshis', 'wallet', 'timest'],
    'use_cols': (0, 1, 3, 4),
    'skip_rows': 1,
    'convert': {
        '0': convert_sha256,
        '3': convert_basestring,
        '4': convert_timestamp
    }
}
