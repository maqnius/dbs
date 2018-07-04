import sys

import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(color_codes=True)

from psycopg2.extras import execute_values
from db import db
from graph import *


def calc_lower_bound(result, vol=0.90):
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

    # Descending sort
    result[::-1].sort()

    acc = 0
    for i, res in enumerate(result):
        acc += res
        if acc / total > vol:
            print('Lower bound for satoshi transaction of {} is enough to have {} % of transaction vol. '
                  'Use of {} % of items ({}).'
                  .format(res, int(vol * 100), int(i / len(result) * 100), i))
            return res


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


def get_user_incomes():
    """
    Calculates sum of incoming money to users (wallets according to users table).

    Returns
    -------

    """
    cur = db.cursor()

    query = """
    select sum(t.satoshis) as sat, u.userid
    from  (
        select sum(ohne.satoshis) as satoshis, ohne.wallet as wallet
        from (
            select satoshis, wallet
            from txoutput
            except 
            select o.satoshis, o.wallet
            from txoutput o, txinput i
            where (o.txid = i.txid and o.wallet = i.wallet)
        ) ohne group by wallet
    ) t, users u
    where t.wallet = u.wallet
    group by u.userid order by sat desc;
    """

    cur.execute(query)
    res = cur.fetchall()
    cur.close()

    return res


def get_wallet_incomes():
    """
    Calculates sum of incoming money to users (wallets according to users table).

    Returns
    -------

    """
    cur = db.cursor()

    query = """
        select sum(ohne.satoshis) as satoshis, ohne.wallet as wallet
        from (
            select satoshis, wallet
            from txoutput
            except 
            select o.satoshis, o.wallet
            from txoutput o, txinput i
            where (o.txid = i.txid and o.wallet = i.wallet)
        ) ohne group by wallet order by satoshis desc;
    """

    cur.execute(query)
    res = cur.fetchall()
    cur.close()

    return res


def get_user_transactions():
    """
    Fetches transactions between users.

    Returns
    -------
    res: array of tuples
        Query result. It cointains
            userid (from)
            userid (to)
            satoshis transferred
            timestamp
            transaction_id
    """
    cur = db.cursor()

    query = """
    select distinct u.userid, outputs.userid, outputs.satoshis, outputs.timest, outputs.txid
    from (
            select u.userid as userid, ohne.txid as txid, ohne.satoshis as satoshis, ohne.timest as timest 
            from (
                select *
                from txoutput
                except 
                select o.*
                from txoutput o, txinput i
                where (o.txid = i.txid and o.wallet = i.wallet)
            ) ohne, users u 
            where u.wallet = ohne.wallet
        ) outputs, txinput i, users u
    where i.txid = outputs.txid and i.wallet = u.wallet and u.userid <> outputs.userid;
    """

    cur.execute(query)
    res = cur.fetchall()
    cur.close()

    return res


def get_wallet_transactions():
    """
    Fetches transactions between users.

    Returns
    -------
    res: array of tuples
        Query result. It cointains
            userid (from)
            userid (to)
            satoshis transferred
            timestamp
            transaction_id
    """
    cur = db.cursor()

    query = """
    select distinct i.wallet, outputs.wallet, outputs.satoshis, outputs.timest, outputs.txid
    from (
            select *
            from txoutput
            except 
            select o.*
            from txoutput o, txinput i
            where (o.txid = i.txid and o.wallet = i.wallet)
        ) outputs, txinput i
    where i.txid = outputs.txid and i.wallet <> outputs.wallet;
    """

    cur.execute(query)
    res = cur.fetchall()
    cur.close()

    return res


def get_users():
    cur = db.cursor()
    cur.execute("""
    select distinct userid
    from users;
    """)

    res = cur.fetchall()
    cur.close()

    return [int(r[0]) for r in res]


if __name__ == '__main__':
    if '--create-users' in sys.argv:
        wallet_u, no_names = cluster_users()
        create_user_table(wallet_u)

    # Distribution of incomes of users
    print('Calculting total user incomes..')
    # incomes = get_wallet_incomes()
    incomes = get_user_incomes()

    # Transactions between users
    print('Getting transactions between users..')
    # transactions = get_wallet_transactions()
    transactions = get_user_transactions()

    print('Creating graph..')
    g = create_graph(incomes, transactions)
    print("Nodes: ", g.num_vertices())
    print("Edges: ", g.num_edges())

    sat = np.array([_[0] for _ in incomes])

    # Lowerbound on user incomes
    # calc_lower_bound(sat, 0.95)
    # calc_lower_bound(sat, 0.90)
    # calc_lower_bound(sat, 0.85)
    limit = calc_lower_bound(sat, 0.40)
    add_lower_income_limit(g, limit)

    print('Filterint Nodes')
    print("Nodes: ", g.num_vertices())
    print("Edges: ", g.num_edges())

    print('Plotting graph..')
    pos = sfdp_layout(g, vweight=g.vp.vweight, C=.2)
    graph_draw(g, pos=pos, vertex_size=g.vp.vsize, output='user_filtered_weights.png')
    graph_draw(g, vertex_size=g.vp.vsize, output='user_filtered.png')

    # sns.distplot(sat, kde=False)
    # plt.show()

    g.set_vertex_filter(None)

    # Lower bound on user transactions
    transaction_volumes = np.array([res[2] for res in transactions], dtype=np.int64)
    transaction_limit = calc_lower_bound(transaction_volumes, 0.40)

    add_lower_transaction_limit(g, transaction_limit)

    print('Filtering Transactions')
    print("Nodes: ", g.num_vertices())
    print("Edges: ", g.num_edges())

    print('Plotting graph..')
    pos = sfdp_layout(g, vweight=g.vp.vweight, C=.2)
    graph_draw(g, pos=pos, vertex_size=g.vp.vsize, output='transactions_filtered_weights_sfdp.png')
    graph_draw(g, vertex_size=g.vp.vsize, output='transactions_filtered.png')
