ERCODE = {
    '0': 'Emphty field',
    '1': 'Basestring is not between 27 and 34 characters long',
    '2': 'Time is in future',
    '3': 'No valid hash',
    '4': 'Database error'
}


class ParseException(Exception):
    def __init__(self, message, code):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.code = code


def error_stat(errors):
    stat = 'Evaluation of Errors:\n'

    for ercode, num in enumerate(errors):
        stat += '{}: {}\n'.format(ERCODE[str(ercode)], num)

    return stat

