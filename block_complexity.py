import sys

import requests


def script_complexity(node, script, function="verifierComplexity"):
    response = requests.post(f'{node}/utils/script/estimate', script).json()
    if response:
        if function == "verifierComplexity":
            if 'verifierComplexity' in response:
                return response['verifierComplexity']
        elif 'callableComplexities' in response and function in response['callableComplexities']:
            return response['callableComplexities'][function]
    return 0


def script_complexity_before_tx(node, address, tx_id):
    response = requests.get(f'{node}/transactions/address/{address}/limit/100').json()
    if response:
        for item in response[0]:
            if 'type' in item and item['type'] == 13:
                if 'id' in item and item['id'] == tx_id:
                    continue
                return script_complexity(node, item['script'])
    return 0


def call_complexity_before_tx(node, tx_id, dapp, call):
    seen = False
    last_id = None
    while True:
        prev_last_id = last_id
        if last_id:
            response = requests.get(f'{node}/transactions/address/{dapp}/limit/1000', params={'after': last_id}).json()
        else:
            response = requests.get(f'{node}/transactions/address/{dapp}/limit/1000').json()
        if response:
            print('.', end="")
            for item in response[0]:
                if 'type' in item:
                    if item['type'] == 16 and item['id'] == tx_id:
                        seen = True
                    if item['type'] == 13:
                        if not seen:
                            continue
                        return script_complexity(node, item['script'], call)
                last_id = item['id']
        else:
            return 0
        if prev_last_id == last_id:
            break
    return 0


def tx_complexity(node, tx):
    if 'type' in tx and 'id' in tx:
        if tx['type'] == 13:
            if 'sender' in tx:
                return script_complexity_before_tx(node, tx['sender'], tx['id'])
        elif tx['type'] == 16:
            if 'dApp' in tx and 'call' in tx:
                return call_complexity_before_tx(node, tx['id'], tx['dApp'], tx['call']['function'])
    return 0


def estimate_block_complexity(node, block_id):
    response = requests.get(f'{node}/blocks/{block_id}').json()
    if response:
        if 'transactions' in response:
            complexity = 0
            for tx in response['transactions']:
                tx_c = tx_complexity(node, tx)
                if tx_c > 0:
                    complexity += tx_complexity(node, tx)
                    print(f'[{tx["id"]}\t:\t{tx_c};\tTotal: {complexity}')
            return complexity
    return 0


if __name__ == '__main__':
    node_param = sys.argv[1]
    block_id_param = sys.argv[2]

    c = estimate_block_complexity(node_param, block_id_param)
    print(f'Estimated complexity of block {block_id_param} is {c}')
