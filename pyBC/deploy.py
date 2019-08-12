import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# web3.py instance
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/bd3f6da3dd35401483729f00acfe5496"))
key="4ef2380d3bf12607e22889169be4d00695914a8274a1e3a9bfe06ab640bf8b1c"

#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
#key="4ef2380d3bf12607e22889169be4d00695914a8274a1e3a9bfe06ab640bf8b1c"
print(w3.isConnected())

acct = w3.eth.account.privateKeyToAccount(key)

# compile your smart contract with truffle first
truffleFile = json.load(open('../build/contracts/ArchiveCertification.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract= w3.eth.contract(bytecode=bytecode, abi=abi)

#building transaction
construct_txn = contract.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

signed = acct.signTransaction(construct_txn)

tx_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])
