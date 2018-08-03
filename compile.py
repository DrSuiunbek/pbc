import argparse
import os
import subprocess

from subprocess import call

def compile_separate():
    cmd = "docker run -v " + contractsdir + ":/data ethereum/solc:stable --bin --abi --overwrite -o /data /data/" + filename
    print(cmd)
    call(cmd, shell=True)

def comile_combined():
    cmd = "docker run -v " + contractsdir + ":/data ethereum/solc:stable --optimize --combined-json abi,bin,interface /data/" + filename
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    s = process.stdout.readline().rstrip()
    print(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the name of the solidity file")
    args = parser.parse_args()

    filename = args.filename

    cwd = os.getcwd()
    datadir = os.path.join(cwd, "data")
    contractsdir = os.path.join(cwd, "contracts")

    compile_separate()
