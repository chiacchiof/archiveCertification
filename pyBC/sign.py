import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract


# compile your smart contract with truffle first
truffleFile = json.load(open('../build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# web3.py instance
w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/bd3f6da3dd35401483729f00acfe5496"))
print(w3.isConnected())
contract_address = Web3.toChecksumAddress("0x54159d1e0E2C7A387297E61A0621e511Fed04a73")
key="a64b8f032eecb48d4fbe40ce2bac3d9fbf6ebe23a40fead0326041526fc9a7ae"
acct = w3.eth.account.privateKeyToAccount(key)
account_address= acct.address

# Instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# Contract instance
contract_instance = w3.eth.contract(abi=abi, address=contract_address)
# Contract instance in concise mode
#contract_instance = w3.eth.contract(abi=abi, address=contract_address, ContractFactoryClass=ConciseContract)

tx = contract_instance.functions.greet("Hello all  my goody people").buildTransaction({'nonce': w3.eth.getTransactionCount(account_address)})
#Get tx receipt to get contract address
signed_tx = w3.eth.account.signTransaction(tx, key)
#tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(hash.hex())
