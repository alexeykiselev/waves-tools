import sys

import requests


def arrange(n, decimals):
    return n / pow(10, decimals)


def total_balance(txs):
    balance = 0
    for ts, height, tx_id, direction, amount, fee, tx_type, total, sponsor in txs:
        balance += total
        yield height, tx_id, tx_type, amount, fee, direction, total, balance, sponsor


def load_block_headers(node, start, stop):
    headers = requests.get(f'{node}/blocks/headers/seq/{start}/{stop}').json()
    return headers


def list_gs():
    node = sys.argv[1]
    start = int(sys.argv[2])
    stop = int(sys.argv[3])

    blocks = load_block_headers(node, start, stop)
    if blocks:
        for b in blocks:
            print(str(b["height"]) + ": " + b["nxt-consensus"]["generation-signature"])
    else:
        print(blocks)


if __name__ == '__main__':
    list_gs()
