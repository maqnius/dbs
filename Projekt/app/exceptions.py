ERCODE = {
    '0': 'Emphty field',
    '1': 'Basestring is not between 27 and 34 characters long',
    '2': 'Time is in future',
    '3': 'No valid hash',
    '4': 'Database error'
}


ERRS = {}


def reset_errs():
    for key in ERCODE.keys():
        ERRS[key] = 0


class ParseException(Exception):
    def __init__(self, code):
        # Now for your custom code...
        self.code = code


def error_stat(errors):
    stat = 'Evaluation of Errors:\n'

    for ercode, num in errors.items():
        stat += '{}: {}\n'.format(ERCODE[ercode], num)

    return stat

