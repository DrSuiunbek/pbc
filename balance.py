import argparse
import os

from subprocess import call


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("node", help="the node for which the balance enquiry is sent")
    args = parser.parse_args()

    cwd = os.getcwd()
    datadir = os.path.join(cwd, "data")
    nodedir = os.path.join(datadir, args.node)

    if os.path.isdir(nodedir):
        cmd = "docker run -v " + nodedir + ":/root/.ethereum ethereum/client-go attach --exec 'eth.getBalance(eth.coinbase)'"
        print(cmd)
        call(cmd, shell=True)
    else:
        print("Node " + args.node + " does not exist.")
