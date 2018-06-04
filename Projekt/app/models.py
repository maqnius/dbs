# Temporary models
TXINPUT = ("CREATE TABLE txinput ("
            "id serial primary key, " 
            "txid varchar, "
            "wallet varchar, "
            "timestamp timestamp "
            ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "id serial primary key, "
            "txid varchar, "
            "satoshis bigint, "
            "wallet varchar, "
            "timestamp timestamp "
            ");")


TXBLOCKS = ("CREATE TABLE txblocks ("
            "txid varchar primary key , "
            "blockid varchar , "
            "timestamp timestamp "
            ");")


# Final Models
TXS = ("CREATE TABLE txs ("
        "txid varchar primary key , "
        "blockid varchar , "
        "timestamp bigint "
        ");")


TRANSFER = ("CREATE TABLE transfer ("
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
