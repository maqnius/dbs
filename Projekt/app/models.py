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

WALLETS = ("SELECT DISTINCT walletid into wallets from (select txoutput.wallet as walletid from txoutput union"
            " select txinput.wallet as walletid from txinput) X; "
           "alter TABLE wallets add constraint pk primary key (walletid);")
