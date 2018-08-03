import os
import shutil
import subprocess
import sys

from os import environ
from subprocess import call

from pbc_utils import read_config


def start_bootnode(datadir):
    bootnodefile = os.path.join(datadir, "bootnode.key")
    if not os.path.isfile(bootnodefile):
        cmd = "docker run -it -v " + datadir + ":/root/ ethereum/client-go:alltools-latest bootnode -genkey /root/bootnode.key"
        print(cmd)
        call(cmd, shell=True)

    call("docker stop mybootnode", shell=True)
    call("docker rm mybootnode", shell=True)
    cmd = "docker run --name mybootnode -d --network host -v " + datadir + ":/root/ ethereum/client-go:alltools-latest bootnode -nodekey /root/bootnode.key"
    print(cmd)
    call(cmd, shell=True)

def start_miners(datadir, networkid):
    cmd = "docker run -v " + datadir + ":/root/ ethereum/client-go:alltools-latest bootnode -nodekey /root/bootnode.key -writeaddress"
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    s = process.stdout.readline().decode().rstrip() + "@127.0.0.1:30301"

    counter = 1
    for miner in miners:
        port = "3031" + str(counter)
        rpcport = "855" + str(counter)
        call("docker stop " + miner, shell=True)
        call("docker rm " + miner, shell=True)
        this_dir = os.path.join(datadir, miner)
        cmd = "docker run --name " + miner + " -d --network host -v " + this_dir + ":/root/.ethereum ethereum/client-go --bootnodes \"enode://" + s + "\" --rpc --rpcaddr \"0.0.0.0\" --networkid " + networkid + " --port " + port + " --rpcport " + rpcport + " --mine"
        print(cmd)
        call(cmd, shell=True)
        counter = counter + 1

def start_chain(datadir, networkid):
    cmd = "docker run -v " + datadir + ":/root/ ethereum/client-go:alltools-latest bootnode -nodekey /root/bootnode.key -writeaddress"
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    s = process.stdout.readline().decode().rstrip() + "@127.0.0.1:30301"

    actors = producers + freighters + shops
    counter = 1
    for actor in actors:
        port = "3032" + str(counter)
        rpcport = "856" + str(counter)
        call("docker stop " + actor, shell=True)
        this_dir = os.path.join(datadir, actor)
        call("docker rm " + actor, shell=True)
        cmd = "docker run --name " + actor + " -d --network host -v " + this_dir + ":/root/.ethereum ethereum/client-go --bootnodes \"enode://" + s + "\" --rpc --rpcaddr \"0.0.0.0\" --networkid " + networkid + " --port " + port + " --rpcport " + rpcport
        print(cmd)
        call(cmd, shell=True)
        counter = counter + 1

if __name__ == "__main__":
    dict = read_config('config.json')
    producers = dict['Producers']
    freighters = dict['Freighters']
    shops = dict['Shops']
    miners = dict['Miners']
    networkid = dict['NetworkID']
    password = dict['Password']

    cwd = os.getcwd()
    datadir = os.path.join(cwd, "data")

    start_bootnode(datadir)
    start_miners(datadir, networkid)
    start_chain(datadir, networkid)
