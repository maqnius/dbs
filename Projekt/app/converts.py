import re


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
