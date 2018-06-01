import re
import os
import csv


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
    m = re.search(r'PUSHDATA\(\d+\)\[(.+)\]\s*PUSHDATA\(\d+\)\[(.+)\]', input_string)
    try:
        result = (m.group(1), m.group(2))
    except IndexError:
        return ''
    return result if all(result) else ''


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
    m = re.search(r'PUSHDATA\(\d+\)\[(.+)\]', output_string)
    try:
        return m.group(1) or ''
    except IndexError:
        return ''


def get_file(name):
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


def fill_table(cur, path, table, col_names, skip_rows=0, use_cols=(), convert={}, fill_missing={}):
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


