import numpy
from psycopg2.extras import execute_values
from helpsers import cached
from db import db

MINNECC = 0


def get_unique_transactions(lower_bound=0):
    """
    Queries all transaction, excluding the change

    Returns
    -------
    result: array of tuples

    """
    cur = db.cursor()

    query = """
        SELECT sum(satoshis), wallet
        from txoutput
        where satoshis not in (
            select o.satoshis
            from txinput i
            inner join txoutput o
            on (i.txid = o.txid and i.wallet = o.wallet)
        ) and satoshis > %s group by wallet order by satoshis desc;
    """

    cur.execute(query, (lower_bound,))

    return cur.fetchall()


def wallet_distribution():
    cur = db.cursor()

    query = """
        SELECT sum(satoshis), wallet
        from txoutput
        where satoshis not in (
            select o.satoshis
            from txinput i
            inner join txoutput o
            on (i.txid = o.txid and i.wallet = o.wallet)
        ) group by wallet order by sum(satoshis) desc;
    """

    cur.execute(query)

    result = cur.fetchall()

    # Convert result to numpy array
    satoshis = numpy.array([res[0] for res in result], dtype=numpy.int64)

    # Calculate histogram
    hist, edges = numpy.histogram(satoshis, normed=False)

    # Define

    data = {
        'x': ["{}-{}".format(numpy.format_float_scientific(edges[i], precision=6),
                             numpy.format_float_scientific(edges[i + 1], precision=6))
              for i in range(len(edges) - 1)],
        'y': hist.tolist()
    }

    return data


def no_trans_distribution():
    cur = db.cursor()

    query = """
        SELECT count(satoshis), wallet
        from txoutput
        where satoshis not in (
            select o.satoshis
            from txinput i
            inner join txoutput o
            on (i.txid = o.txid and i.wallet = o.wallet)
        ) group by wallet;
    """

    cur.execute(query)

    result = cur.fetchall()

    # Convert result to numpy array
    satoshis = numpy.array([res[0] for res in result], dtype=numpy.int64)

    # Calculate histogram
    hist, edges = numpy.histogram(satoshis, normed=False)

    # Define

    data = {
        'x': ["{}-{}".format(int(edges[i]),
                             int(edges[i + 1]))
              for i in range(len(edges) - 1)],
        'y': hist.tolist()
    }

    return data


@cached
def trans_distribution():
    global MINNECC

    result = get_unique_transactions()

    # Convert result to numpy array
    satoshis = numpy.array([res[0] for res in result], dtype=numpy.int64)

    # Calculate histogram
    hist, edges = numpy.histogram(satoshis, bins=10, normed=False)

    # Define
    data = {
        'x': ["{}-{}".format(numpy.format_float_scientific(edges[i], precision=6),
                             numpy.format_float_scientific(edges[i + 1], precision=6))
              for i in range(len(edges) - 1)],
        'y': hist.tolist()
    }

    MINNECC = int(_calc_useful_data(satoshis))

    return data


def _calc_useful_data(result, vol=0.90):
    """
    Sum up n biggest amounts of transactions until volume is at least
    90 % of the maximum

    Parameters
    ----------
    result
    vol

    Returns
    -------

    """
    total = result.sum()

    acc = 0
    for i, res in enumerate(result):
        acc += res
        if acc / total > vol:
            print('Lower bound for satoshi transaction of {} is enough to have {} % of transaction vol. '
                  'Use of {} % of items ({}).'
                  .format(res, int(vol * 100), int(i / len(result) * 100), i))
            return res


def get_range():
    """
    Get min max

    Returns
    -------

    """
    cur = db.cursor()

    # Get max and min amount of transaction
    cur.execute("SELECT MAX(satoshis), MIN(satoshis) FROM txoutput where satoshis > 0;")

    return cur.fetchone()


def cluster_users():
    """
    Clusters users depending on their occurence in inputs

    Returns
    -------
    wallet_u: dictionary
        wallet_id -> userid

    u: number of usernames
    """
    cur = db.cursor()

    # Get all distinc wallet, txid combinations
    # Sort by wallet is important for the algorithm to work!
    query = """
        select distinct wallet, txid
        from txinput order by wallet asc;
    """

    cur.execute(query)
    res = cur.fetchall()
    cur.close()

    # Create a association between wallet name and
    # the transactions in which it occurs
    wallet_txids = {}
    for wallet, txid in res:
        try:
            wallet_txids[wallet].append(txid)
        except KeyError:
            wallet_txids[wallet] = [txid]

    """
    
    Run through all wallets and check the txids in which they
    occur. If there was a wallet before, included in one of its
    transcaction inputs, we assign to the current wallet and all
    its transactoins the same userid.
    
    If this transaction has never been 'touched' before, we assing to 
    this wallet and all its transactions a new userid.
    
    """
    u = 0  # userid
    txid_u = {}  # txid -> username
    wallet_u = {}  # walletid -> username

    for w, txids in wallet_txids.items():
        found = False

        for txid in txids:
            if txid in txid_u:
                uname = txid_u[txid]
                wallet_u[w] = uname
                add_all(txids, uname, txid_u)
                found = True
                break

        if not found:
            u += 1
            wallet_u[w] = u
            add_all(txids, u, txid_u)

    return wallet_u, u


def add_all(txids, user, txid_u):
    for txid in txids:
        txid_u[txid] = user


def create_user_table(wallet_userid):
    cur = db.cursor()

    cur.execute("""
        create table users(
          wallet varchar(34) primary key,
          userid int
        );
        """)

    execute_values(cur, "insert into users (wallet, userid) values %s", wallet_userid.items())
    db.commit()
    cur.close()


if __name__ == '__main__':
    wallet_u, no_names = cluster_users()
    create_user_table(wallet_u)
