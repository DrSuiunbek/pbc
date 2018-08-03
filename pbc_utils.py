import json
import rlp

from Crypto.Hash import keccak

def generate():
    data = {
            'Producers': ['P1', 'P2', 'P3'],
            'Freighters': ['F1', 'F2'],
            'Shops': ['S1', 'S2'],
            'Miners': ['M1'],
            'NetworkID': '2003',
            'Password': '12345'
           }
    jstr = json.dumps(data, indent=4)
    print(jstr)

def read_config(filename):
    with open(filename) as inputfile:
        data = json.load(inputfile)

    if not 'Producers' in data:
        print('Producers input is missing.')
        return None

    if not 'Freighters' in data:
        print('Freighters input is missing.')
        return None

    if not 'Shops' in data:
        print('Shops input is missing.')
        return None

    if not 'Miners' in data:
        print('Miners input is missing.')
        return None

    if not 'NetworkID' in data:
        print('NetworkID input is missing.')
        return None

    if not 'Password' in data:
        print('Password input is missing.')
        return None

    return data


def normalize_address(x, allow_blank=False):
    if allow_blank and x == '':
        return ''
    if len(x) in (42, 50) and x[:2] == '0x':
        x = x[2:]
    if len(x) in (40, 48):
        x = rlp.utils.decode_hex(x)
    if len(x) != 20:
        raise Exception("Invalid address format: %r" % x)
    return x


def mk_contract_address(sender, nonce):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(rlp.encode([normalize_address(sender), nonce]))
    return keccak_hash.hexdigest()[24:]

