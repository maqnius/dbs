# Temporary models
TXINPUT = ("CREATE TABLE txinput ("
            "txid char(64), "
            "wallet varchar(34), "
            "timest timestamp "
            ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "txid char(64), "
            "satoshis bigint, "
            "wallet varchar(34), "
            "timest timestamp "
            ");")


TXBLOCKS = ("CREATE TABLE txblocks ("
            "txid char(64) primary key , "
            "blockid char(64) , "
            "timest timestamp "
            ");")


# Final Models
TXS = ("SELECT txid, blockid, timest from txblocks where txid in (select distinct txid from tranfer)")


TRANSFER = ("SELECT input.txid, input.wallet as wallet_in, output.wallet as wallet_out, output.satoshis, output.timest "
            "INTO transfer "
            "FROM txinput as input "
            "INNER JOIN txoutput as output ON input.txid = output.txid;"
            )

# TODO: Add User ID
WALLETS = ("SELECT DISTINCT walletid into wallets from (select distinct transfer.wallet_in as walletid from transfer union "
            " select distinct transfer.wallet_out as walletid from transfer) X;")

PREP_WALLETS = ("CREATE TABLE wallets ("
            "walletid char(64) primary key, "
            "userid serial unique;")


# Necessary at this point?
USERS = ("")


