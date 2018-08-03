import os
import shutil
import sys

from subprocess import call

from pbc_utils import read_config

def stop_bootnode():
    call("docker stop mybootnode", shell=True)
    call("docker rm mybootnode", shell=True)

def stop_miners():
    for miner in miners:
        call("docker stop " + miner, shell=True)
        call("docker rm " + miner, shell=True)

def stop_chain():
    actors = producers + freighters + shops
    for actor in actors:
        call("docker stop " + actor, shell=True)
        call("docker rm " + actor, shell=True)

if __name__ == "__main__":
    dict = read_config('config.json')
    producers = dict['Producers']
    freighters = dict['Freighters']
    shops = dict['Shops']
    miners = dict['Miners']

    stop_bootnode()
    stop_miners()
    stop_chain()
