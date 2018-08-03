import os
import shutil
import sys

from os import environ
from subprocess import call

from pbc_utils import read_config


def is_toolbox():
    if environ.get('DOCKER_TOOLBOX_INSTALL_PATH') is not None:
        return True
    return False

def make_toolbox_path(path):
    return path.replace('C:', '\\c').replace('\\', '/')

def create_accounts(datadir):
    if os.path.isdir(datadir):
        print("deleting: " + datadir)
        shutil.rmtree(datadir)

    os.makedirs(datadir)

    password_filename = os.path.join(datadir, "passwd")
    f = open(password_filename, "w")
    f.write(password)
    f.close()

    actors = producers + freighters + shops + miners
    for actor in actors:
        actor_path = os.path.join(datadir, actor)
        datadir2 = datadir
        os.makedirs(actor_path)

        if is_toolbox():
            actor_path = make_toolbox_path(actor_path)
            datadir2 = make_toolbox_path(datadir)

        cmd = "docker run -it -v " + actor_path + ":/root/.ethereum -v " + datadir2 + ":/data ethereum/client-go account new --password /data/passwd"
        print(cmd)
        call(cmd, shell=True)


def create_genesis(datadir):
    actors = producers + freighters + shops + miners
    accounts = []
    for actor in actors:
        actor_path = os.path.join(datadir, actor, "keystore")
        for file in os.listdir(actor_path):
            accounts.append(file[-40:])

    genesis_head = \
    '{\n'\
    '    "config": {\n'\
    '        "chainId": ' + networkid + ',\n'\
    '        "homesteadBlock": 0,\n'\
    '        "eip155Block": 0,\n'\
    '        "eip158Block": 0\n'\
    '    },\n'\
    '    "difficulty": "2000",\n'\
    '    "gasLimit": "2100000",\n'\
    '    "alloc": {\n'

    genesis_tail = \
    '    }\n'\
    '}\n'

    genesis_filename = os.path.join(datadir, "genesis.json")
    f = open(genesis_filename, "w")
    counter = 0
    f.write(genesis_head)
    for account in accounts:
        counter = counter + 1
        if counter < len(accounts):
            f.write('        "' + account + '": { "balance": "5000000000000000000" },\n')
        else:
            f.write('        "' + account + '": { "balance": "5000000000000000000" }\n')
    f.write(genesis_tail)
    f.close()

    for actor in actors:
        actor_path = os.path.join(datadir, actor)
        datadir2 = datadir

        if is_toolbox():
            actor_path = make_toolbox_path(actor_path)
            datadir2 = make_toolbox_path(datadir)
        cmd = "docker run -it -v " + actor_path + ":/root/.ethereum -v " + datadir2 + ":/data ethereum/client-go init /data/genesis.json"
        print(cmd)
        call(cmd, shell=True)


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

    create_accounts(datadir)
    create_genesis(datadir)
