from converts import convert_input_string, convert_output_string


TXINPUT = ("CREATE TABLE txinput ("
           "txid varchar PRIMARY KEY, "
           "walletid varchar, "
           "walletsign varchar, "
           "timestamp bigint "
           ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "txid varchar PRIMARY KEY, "
            "satoshis bigint, "
            "walletid varchar, "
            "timestamp bigint "
            ");")


TXBLOCKS = ("CREATE TABLE txblocks ("
            "txid varchar PRIMARY KEY, "
            "blockid varchar, "
            "timestamp bigint "
            ");")


CONF_TXBLOCKS = {
    'table': 'txblocks',
    'col_names': ['txid', 'blockid', 'timestamp'],
    'use_cols': (0, 1, 6),
    'skip_rows': 1
}


CONF_TXINPUT = {
    'table': 'txinput',
    'col_names': ['txid', 'walletid', 'walletsign', 'timestamp'],
    'use_cols': (0, 1, 4),
    'skip_rows': 1,
    'convert': {
        '1': convert_input_string
    }
}


CONF_TXOUTPUT = {
    'table': 'txoutput',
    'col_names': ['txid', 'satoshis', 'walletid', 'timestamp'],
    'use_cols': (0, 1, 2, 4),
    'skip_rows': 1,
    'convert': {
        '2': convert_output_string
    }
}
