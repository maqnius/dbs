# Temporary models
TXINPUT = ("CREATE TABLE txinput ("
            "id serial primary key, " 
            "txid varchar, "
            "walletid varchar, "
            "walletsign varchar, "
            "timestamp bigint "
            ");")


TXOUTPUT = ("CREATE TABLE txoutput ("
            "id serial primary key, "
            "txid varchar, "
            "satoshis bigint, "
            "walletid varchar, "
            "timestamp bigint "
            ");")


TXBLOCKS = ("CREATE TABLE txblocks ("
            "txid varchar, "
            "blockid varchar PRIMARY KEY , "
            "timestamp bigint "
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
