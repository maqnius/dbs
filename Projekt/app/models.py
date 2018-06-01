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

