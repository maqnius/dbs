import psycopg2
import os
import configparser
from appconfig import config
"""
This is where the magic happens!

"""


def init_db(config):

    # Connect to database
    db = psycopg2.connect(**config)
    return db


def _create_tables(db):
    # Create tables
    # Fill with content
    pass


def _parse_files(db):
    DATA = './data'
    FILE_BLOCKS = os.path.join(DATA, 'transactions_blocks.csv')
    FILE_INPUT = os.path.join(DATA, 'transactions_input.csv')
    FILE_OUTPUT = os.path.join(DATA, 'transactions_output.csv')


if __name__ == '__main__':
    db = init_db(config['database'])
    _create_tables(db)
    _parse_files(db)
