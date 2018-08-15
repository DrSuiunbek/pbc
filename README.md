# A Private Ethereum Network

The purpose of this project is to give an introduction to Ethereum network and to smart contracts. In the scope of the Ethereum network we learn the structure of the network and its participants. In smart contract section we will write our first smart contract and learn how to deploy it. We will also learn how to call the smart contract’s methods. The smart contract we write is for tracking the produce. We will learn how to transfer the ownership and how to record the tracking data. To achieve the platform independence we use Docker CE on host systems with the support of virtualisation, e.g. Mac OS, Linux, Windows 10 Professional.

# Docker
Docker offers container platform. In other words it offers a platform to run containers, a prepackaged software blocks, which will be executed exactly the same way on all computers. The latest Docker CE relies on the virtualisation support of the CPU and the host operating system. Some slimmed down operating systems, like Windows 10 Home, do not support the virtualisation although the hardware does.
If your operating system supports virtualisation please install Docker CE from https://www.docker.com/community-edition. To run this project you need three images:

• ethereum/client-go:alltools-latest

• ethereum/client-go:latest

• ethereum/solc:stable

In order to get them execute the following commands

  $ docker pull ethereum/client-go:alltools-latest
  
  $ docker pull ethereum/client-go:latest
  
  $ docker pull ethereum/solc:stable
  
Once the command is complete check if the images are indeed downloaded by executing the command

  $ docker image ls
  
The output should be something like this

REPOSITORY          TAG               IMAGE ID      CREATED         SIZE

ethereum/client-go  alltools-latest   8b21c6ca2561  7 weeks ago     313MB

ethereum/client-go  latest            ea79fda0b03a  8 weeks ago     42.4MB

ethereum/solc       stable            8f6f71d13bb4  2 months ago    14.3MB


We have the necessary Docker images. Now we need the project files. If your system has git you can execute the command

 $ git clone https://github.com/DrSuiunbek/pbc.git

This will copy the project files from GitHub. Alternatively, you can download the archive of project files directly.

# Private Blockchain
We use Python 3 to set up and interact with the network. We need two packages which are not included in the standard Python distribution. Install them executing

$ pip3 install pycryptodome

$ pip3 install rlp==0.6.0

The private network is configured using config.json configuration file. It is in JSON format and lists network participants:

• Producers;

• Feighters;

• Ships;

• Miners.


The configuration file also contains the network ID and the password common for all accounts. All participants except Miners are the same. Miners perform one extra task: mining. One miner is sufficient to run this private network.

# Accounts

Each node in the blockchain network requires at least one account. To create accounts according the configuration file execute

$ python3 create_accounts.py

This will create a folder called *data* and inside one folder per network participant. Each participant has its own full blockchain copy in its folder. The blockchain is initialised with the so called genesis file. It contains all created accounts and their balances. The Python script calls Go Ethereum client *geth* with the following argument:

account new --password passwordfile

Omitting *–password passwordfile* will prompt for password. Once all accounts are created Python script generates genesis.json file and calls geth with arguments

init genesis.json

Right now all nodes have been initialised with the same genesis.json. They may differ. When the very first block gets mines its content will be used as the state of the network.

# Bootnode
When the active node of the Ethereum network starts it needs to connect to peers. It is made possible through the use of so called bootnodes. The public Ethereum network has the static bootnodes. They have the form

 "enode://bootkey@ip_address:port"

Since we are setting up our private network we need to have our own bootnodes. For this we generate bootnode key by calling

$ bootnode -genkey bootnode.key

This creates bootnode.key file with the key. Using this key we start the bootnode for our private network

 $ bootnode -nodekey bootnode.key
 
Since we are running the network on our local machine the IP address will be of our local host:

127.0.0.1

We will keep the standard port number 30301.

# Starting and Stopping the Network

To start the network we geth passing it enode information. For mininers we additionally pass *–mine*. This all is achieved by executing the command

 $ python3 start_network.py
 
The network is stopped simply by terminating all running programs. In the command shell simply execute:

 $ python3 stop_network.py


# Smart Contract

In this project we use a simple smart contract called ProofOfProduce. Our smart contract has two methods:

• storeProof
• transfer

The former method is to store the proof of produce by the owner. The latter is to transfer the ownership. Before the smart contract is deployed it needs to be complied. We use the standard Solidity compiler solc. To compile ProofOfProduce.sol execute

 $ python3 compile.py ProofOfProduce.sol

It creates two files

• ProofOfProduce.abi

• ProofOfProduce.bin

The first file is the application binary interface. It is a JSON file describing the smart contract. It is used in order to call the smart contract from any active node. The second file is the binary code of the smart contract. This is the file which gets deployed. The contract can be deployed by

 $ python3 deploy.py node
 
Here the node is the name of any node. This is because our smart contract can be deployed by any node not necessarily the producer. The smart contract address depends on the node address and the number of smart contracts it has deployed. We can display the smart contract address by calling

 $ python3 address.py node nonce
 
Here the node is the name of the node which deploys the smart contract. The nonce is the cardinal number indicating how many smart contracts the node had deployed so far, e.g. 0 if we are deploying the very first smart contract. Once the smart contract is mined its address will become available to interact. We can call storeProof or transfer now. To call storeProof execute

 $ python3 call_store.py contractnode contractnonce owner tr_id prev_id proof_enc proof_pub
 
We need contractnode and contractnonce in order to determine the smart contract address. The owner is the name of the node storing the proof. The tr id is the tracking ID under which the proof is stored. To start a new chain of supply we need to pass root as the prev id, otherwise it is the ID of the previous transaction. To transfer the ownership simply call

 $ python3 call_transfer.py contractnode contractnonce owner tr_id new_owner
 
Consider the following scenario

• Node P1 deploys the smart contract;

• Node P2 initiates the supply chain by storing the initial proof of produce;

• Node P2 transfers the ownership to F1;

• Node F1 stores its transaction details;

• Node F1 transfers the ownership to S1;

• Node S1 stores its transaction details.
   
This is achieved by
 $ python3 deploy.py P1
 
 $ python3 call_store.py P1 0 P2 "tr_1" "root" "proof_enc_1" "proof_pub_1"
 
 $ python3 call_transfer P1 0 P2 "tr_1" F1
 
 $ python3 call_store.py P1 0 F1 "tr_2" "tr_1" "proof_enc_2" "proof_pub_2"
 
 $ python3 call_transfer P1 0 F1 "tr_2" S1
 
 $ python3 call_store.py P1 0 S1 "tr_3" "tr_2" "proof_enc_3" "proof_pub_3"
