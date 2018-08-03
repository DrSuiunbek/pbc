import argparse
import os

from subprocess import call

from pbc_utils import read_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contract_node", help="the node which published the smart contract", type=str)
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
    contractdir = os.path.join(cwd, "contracts")

    this_dir = os.path.join(datadir, args.contract_node)
    if not os.path.isdir(this_dir):
        print("Node " + args.contract_node + " does not exist.")
        sys.exit(1)

    cmd = "docker run -v " + this_dir + ":/root/.ethereum ethereum/client-go attach --exec 'personal.unlockAccount(eth.coinbase, \"" + password + "\", 3000)'"
    print(cmd)
    call(cmd, shell=True)

    contract_abi = os.path.join(contractdir, "ProofOfProduce.abi")
    contract_bin = os.path.join(contractdir, "ProofOfProduce.bin")
    script = open(os.path.join(contractdir, "deploy.js"), "w")
    f = open(contract_abi, "r")
    abi = f.read()
    f.close()
    f = open(contract_bin, "r")
    bin = f.read()
    f.close()

    script.write("var contract = eth.contract(" + abi + ")\n")
    script.write("var bytecode = '0x" + bin + "'\n")
    script.write("var deploy = {from:eth.coinbase, password: \"" + password + "\", data:bytecode, gas: 2000000}\n")
    script.write("var obj = contract.new(deploy)\n")
    script.close()

    cmd = "docker run -it -v " + this_dir + ":/root/.ethereum -v " + contractdir + ":/data ethereum/client-go attach --jspath /data --exec 'loadScript(\"deploy.js\")'"
    print(cmd)
    call(cmd, shell=True)

