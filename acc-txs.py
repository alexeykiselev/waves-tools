import requests


def load_block(height):
    block = requests.get(f"https://nodes.wavesnodes.com/blocks/at/{height}").json()[0]
    for tx in block['transactions']:
        if tx['type'] == 16 and tx['dApp'] == "3PNASfdCWXvYfErZXoKhVbi7XrbJw1SJvfg":
            print(height, ":", tx['id'])
            return True


if __name__ == '__main__':
    h = 4_090_000
    stop = False
    while not stop:
        print(".")
        load_block(h)
        h += 1
