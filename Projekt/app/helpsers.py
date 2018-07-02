import csv
import random

_names = []
_used = set({})

with open('./data/CSV_Database_of_First_Names.csv') as file:
    reader = csv.reader(file)
    for name in reader:
        _names.append(name[0].strip())


def get_uniqe_name():
    """
    Creates names that are unique (during runtime of creation)

    Returns
    -------
    str
        Unique surname

    """
    name = random.choice(_names)

    while name in _used:
        name = random.choice(_names)

    _used.add(name)

    return name


CACHE = {}


def cached(func):
    global CACHE

    def data(*args, **kwargs):
        try:
            return CACHE[func.__name__]
        except KeyError:
            CACHE[func.__name__] = func(*args, **kwargs)
            return CACHE[func.__name__]

    return data
