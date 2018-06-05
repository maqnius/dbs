# Temporary models
TXINPUT = ("CREATE TABLE txinput ("
            "txid char(64), "
            "wallet char(34), "
            "timestamp timestamp "
            ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "txid char(64), "
            "satoshis bigint, "
            "wallet varchar(34), "
            "timestamp timestamp "
            ");")


TXBLOCKS = ("CREATE TABLE txblocks ("
            "txid char(64) primary key , "
            "blockid char(64) , "
            "timestamp timestamp "
            ");")


# Final Models
TXS = ("")


TRANSFER = ("SELECT input.txid, input.wallet as wallet_in, output.wallet as wallet_out, output.satoshis, output.timestamp "
            "INTO transfer "
            "FROM txinput as input "
            "FULL OUTER JOIN txoutput as output ON input.txid = output.txid;"
            )


WALLETS = ("")


USERS = ("")


