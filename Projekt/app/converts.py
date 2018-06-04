import re
import os
import csv
from psycopg2 import IntegrityError


def convert_input_string(input_string):
    """
    Searches an input string for signature and pubkey

    TODO:
        - Hash pubkey to get walletid

    Parameters
    ----------
    input_string

    Returns
    -------
    tuple | ''
        First element is the signature, the second is the pubkey.
        If any of both is not found, an empty string is returned in order
        to mark an falsy column value.

    """
    keys = re.findall(r'\[(\w+)\]', input_string)

    if len(keys) == 2:
        return keys
    if len(keys) == 1:
        return keys + ['']
    else:
        raise TypeError(input_string)


def convert_output_string(output_string):
    """
    Searches an output string for the walletid

    Parameters
    ----------
    output_string: str
        Bitcoin output string

    Returns
    -------
    str | ''
        Returns the walletid or an empty string to mark falsy column value

    """
    keys = re.findall(r'\[(.+)\]', output_string)

    if len(keys) == 2:
        return keys
    elif len(keys) == 1:
        return keys + ['']
    else:
        raise TypeError(output_string)


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


def fill_table(db, path, table, col_names, skip_rows=0, use_cols=(), convert={}, fill_missing={}):
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
    cur = db.cursor()

    execute_string = "INSERT INTO {} ({}) VALUES ({})".format(
        table,
        ','.join(col_names),
        ','.join(['%s']*len(col_names))
    )

    errors = []
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
            except (IndexError, TypeError):
                # Not all columns could be parsed
                errors.append(row)
                print("Error during parsing: " + ', '.join(row))
            except IntegrityError:
                # Already entry in table
                errors.append(row)
                print("Already exists: " + ', '.join(row))
                db.rollback()

    return errors


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
                    raise TypeError(column)

            except TypeError as e:
                if str(ix) in fill_missing:
                    # Fill if for this column there is a fill value given
                    entries += fill_missing[str(ix)]
                else:
                    raise e

    return entries


CONF_TXBLOCKS = {
    'path': _get_file('transactions_blocks.csv'),
    'table': 'txblocks',
    'col_names': ['txid', 'blockid', 'timestamp'],
    'use_cols': (0, 1, 6),
    'skip_rows': 1
}


CONF_TXINPUT = {
    'path': _get_file('transactions_input.csv'),
    'table': 'txinput',
    'col_names': ['txid', 'walletid', 'walletsign', 'timestamp'],
    'use_cols': (0, 1, 4),
    'skip_rows': 1,
    'convert': {
        '1': convert_input_string
    }
}


CONF_TXOUTPUT = {
    'path': _get_file('transactions_output.csv'),
    'table': 'txoutput',
    'col_names': ['txid', 'satoshis', 'walletid', 'timestamp'],
    'use_cols': (0, 1, 2, 4),
    'skip_rows': 1,
    'convert': {
        '2': convert_output_string
    }
}
