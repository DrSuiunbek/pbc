import argparse
import os
import sys

from subprocess import call

from pbc_utils import mk_contract_address
from pbc_utils import read_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contract_node", help="the node which published the smart contract", type=str)
    parser.add_argument("contract_nonce", help="the nonce for smart contract", type=int)
    parser.add_argument("owner", help="the node which is calling the function", type=str)
    parser.add_argument("tracking_id", help="", type=str)
    parser.add_argument("new_owner", help="", type=str)
    args = parser.parse_args()

    dict = read_config('config.json')
    producers = dict['Producers']
    freighters = dict['Freighters']
    shops = dict['Shops']
    miners = dict['Miners']
    networkid = dict['NetworkID']
    password = dict['Password']

    cwd = os.getcwd()
    datadir = os.path.join(cwd, "data")
    contract_node_path = os.path.join(datadir, args.contract_node, "keystore")
    owner_path = os.path.join(datadir, args.owner)
    new_owner_path = os.path.join(datadir, args.new_owner, "keystore")

    if not os.path.isdir(contract_node_path):
        print("Node " + args.contract_node + " does not exist.")
        sys.exit(1)
    if not os.path.isdir(owner_path):
        print("Node " + args.owner + " does not exist.")
        sys.exit(1)
    if not os.path.isdir(new_owner_path):
        print("Node " + args.new_owner + " does not exist.")
        sys.exit(1)

    contract_node = os.listdir(contract_node_path)[0][-40:]
    contract_nonce = args.contract_nonce
    contract_address = mk_contract_address(contract_node, contract_nonce)

    new_owner = os.listdir(contract_node_path)[0][-40:]

    contract_dir = os.path.join(cwd, "contracts")
    contract_abi = os.path.join(contract_dir, "ProofOfProduce.abi")
    f = open(contract_abi, "r")
    abi = f.read()
    f.close()
    script = open(os.path.join(contract_dir, "call_transfer.js"), "w")
    script.write("var contract = eth.contract(" + abi + ")\n")
    script.write("var contract_instance = contract.at('0x" + contract_address + "')\n")
    script.write("var trackingId = '" + args.tracking_id + "'\n")
    script.write("var newOwner = 0x" + new_owner + "\n")
    script.write("contract_instance.transfer(trackingId, newOwner)\n")
    script.close()

    this_dir = os.path.join(datadir, args.owner)

    cmd = "docker run -v " + this_dir + ":/root/.ethereum -v " + contract_dir + ":/data ethereum/client-go attach --jspath /data --exec 'eth.defaultAccount=eth.coinbase; personal.unlockAccount(eth.coinbase, \"" + password + "\", 3000); loadScript(\"call_transfer.js\")'"
    print(cmd)
    call(cmd, shell=True)

