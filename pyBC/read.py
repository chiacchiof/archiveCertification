import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract


# compile your smart contract with truffle first
truffleFile = json.load(open('../build/contracts/ArchiveCertification.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
print (abi)
# web3.py instance
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/bd3f6da3dd35401483729f00acfe5496"))
key="f2ff54dfe3297c9d049d3d9fcc94f3b09a533593dc0cf51db89077e7259de66c"
contract_address = Web3.toChecksumAddress("0xbd8D5183388aEB2BDc96B3c2Ba57ca97F25c5A97")

#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
#key="f2ff54dfe3297c9d049d3d9fcc94f3b09a533593dc0cf51db89077e7259de66c"
#contract_address = Web3.toChecksumAddress("0x71eeb9099daf07d743ef51e42aec862c3c106532")

print(w3.isConnected())


# Instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# Contract instance
contract_instance = w3.eth.contract(abi=abi, address=contract_address)
# Contract instance in concise mode
#contract_instance = w3.eth.contract(abi=abi, address=contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object ConciseContract
#print('Contract value: {}'.format(contract_instance.functions.getGreeting().call()))
certificate = contract_instance.functions.getContractOwner();
print(certificate.call())
