# Temporary models
TXINPUT = ("CREATE TABLE txinput ("
            "id serial primary key, " 
            "txid char(64), "
            "wallet char(34), "
            "timestamp timestamp "
            ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "id serial primary key, "
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
TXS = ("CREATE TABLE txs ("
        "txid char(64) primary key , "
        "blockid char(64) , "
        "timestamp bigint "
        ");")


TRANSFER = ("CREATE TABLE transfer as ("
            "txid varchar, "
            "satoshis bigint, "
            "from_wallet varchar, "
            "to_wallet varchar, "
            "PRIMARY KEY (txid, from_wallet, to_wallet)"
             ");")


WALLETS = ("CREATE TABLE wallets  as ("
            "select distinct walletid, walletsign "
            "from txinput"
            "); ")


USERS = ("CREATE TABLE users ("
           "userid SERIAL PRIMARY KEY , "
           "alias varchar "
           ");")
