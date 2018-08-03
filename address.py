import argparse
import os

from pbc_utils import mk_contract_address

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("node", help="the node which published the smart contract", type=str)
    parser.add_argument("nonce", help="the nonce used for smart contract deployment", type=int)
    args = parser.parse_args()

    cwd = os.getcwd()
    actor_path = os.path.join(cwd, "data", args.node, "keystore")

    if os.path.isdir(actor_path):
        sender = os.listdir(actor_path)[0][-40:]
        print("sender: " + sender)
        nonce = args.nonce
        print('calculated address: 0x' + mk_contract_address(sender, nonce))
    else:
        print("Node " + args.node + " does not exist.")

