import pymysql
import random
import time
from time import sleep
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import datetime
from datetime import datetime
import pyqrcode
import urllib;
from pyqrcode import QRCode
from eth_keys import keys
from eth_utils import decode_hex


class InspectDB():
    def __init__(self):
        self._conn = pymysql.connect(host='127.0.0.1', user='root', password='entra123', db='testDB')
        self._cur = self._conn.cursor()
        self._lastentry = -1;
    def run(self):
        self._cur.execute("SELECT id FROM transactions ORDER BY id DESC LIMIT 1")
        for response in self._cur:
            print(response)
            self._lastentry = response[0]
            self._conn.commit()
        while True:
            self._cur.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 1")
            time.sleep(5)
            for response in self._cur:
                print(self._lastentry)
                print(response[0])
                if(self._lastentry<response[0]):
                    self._lastentry = response[0]
                    value = response[1]
                    description = response[2]
                    prvKey = '4ef2380d3bf12607e22889169be4d00695914a8274a1e3a9bfe06ab640bf8b1c' #this must come from another table
                    priv_key_bytes = decode_hex(prvKey)
                    priv_key = keys.PrivateKey(priv_key_bytes)
                    pubKey = priv_key.public_key
                    addressProcessOwner = pubKey.to_checksum_address()

                    print("ready to write in BC")
                    # compile your smart contract with truffle first
                    truffleFile = json.load(open('../build/contracts/ArchiveCertification.json')) #start this script from the _dummy folder
                    abi = truffleFile['abi']
                    bytecode = truffleFile['bytecode']

                    # web3.py instance
                    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/bd3f6da3dd35401483729f00acfe5496"))
                    privateKey="4ef2380d3bf12607e22889169be4d00695914a8274a1e3a9bfe06ab640bf8b1c"
                    #contract_address = Web3.toChecksumAddress("0x71EEb9099DAf07D743ef51E42AEC862C3c106532")
                    #deployed at Ropsten
                    #Transaction ID: 0x46d562abb2f5b0cb03d6ee445378f87c5848779271aee8faadc3e1a3ddadf80b
                    
                    #w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
                    #privateKey="4ef2380d3bf12607e22889169be4d00695914a8274a1e3a9bfe06ab640bf8b1c"
                    
                    contract_address = Web3.toChecksumAddress("0xbd8D5183388aEB2BDc96B3c2Ba57ca97F25c5A97") 
                    print(w3.isConnected())
                    acct = w3.eth.account.privateKeyToAccount(privateKey)
                    addressContractOwner= acct.address
                    
                    # Instantiate and deploy contract
                    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                    # Contract instance
                    contract_instance = w3.eth.contract(abi=abi, address=contract_address)
                    # Contract instance in concise mode
                    #contract_instance = w3.eth.contract(abi=abi, address=contract_address, ContractFactoryClass=ConciseContract)
                    
                    uniqueIdentifier = random.getrandbits(16);
                    txn0 = {'gas': 3000000, 'nonce': w3.eth.getTransactionCount(addressContractOwner)};
                    #tx = contract_instance.functions.signCertificate(addressProcessOwner, value , description, "§§"+addressProcessOwner, uniqueIdentifier).buildTransaction({'nonce': w3.eth.getTransactionCount(addressContractOwner)})
                    tx = contract_instance.functions.signCertificate(addressProcessOwner, value , description, "§§"+addressProcessOwner, uniqueIdentifier).buildTransaction(txn0)
                    #Get tx receipt to get contract address
                    signed_tx = w3.eth.account.signTransaction(tx, privateKey)
                    #tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
                    hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                    sleep(60)
                    print(hash.hex())
                    ####To add in a Proof of Work network
                    #tsBlock = w3.eth.getTransaction(hash.hex()).blockNumber;
                    #print(tsBlock)
                    #tsTimestamp = datetime.datetime.fromtimestamp(w3.eth.getBlock(tsBlock).timestamp)
                    #### ***** ###########    
                    tsTimestamp = datetime.today()
                    tsTimestampStr = tsTimestamp.strftime('%Y-%m-%d %H:%M:%S')
                    certificateNumber = contract_instance.functions.getNumberOfCertificates().call()

                    transactionQuery = 'UPDATE transactions set addressOwner="'+addressProcessOwner+'", transactionAddress="'+hash.hex()+'", transactionTimestamp = "'+tsTimestampStr+'", uniqueIdentifier =%s, contractID=%s where id=%s'
                    print(certificateNumber)
                    #print (transactionQuery)
                    self._cur.execute(transactionQuery,(uniqueIdentifier, certificateNumber,self._lastentry))
                    #create QRCode
                    params = {'ID': str(certificateNumber),'UniqueIdentifier': uniqueIdentifier ,'Timestamp': tsTimestampStr, 'Transaction': hash.hex()}
                    #QRCodeUrl = pyqrcode.create("http://localhost:3000/?prod=##§##"+str(certificateNumber)+"##§##"+tsTimestampStr+"##§##"+hash.hex())
                    QRCodeUrl = pyqrcode.create("http://localhost:3000?"+urllib.parse.urlencode(params))
                    QRCodeUrl.svg("qrCodeImg/"+str(certificateNumber)+"_"+tsTimestampStr+".svg",scale=8)
                    print(QRCodeUrl);
                    
                self._conn.commit()

        cur.close()
        conn.close()

if __name__ == '__main__':
    InspectDB().run()
