"""
Alpha prototype
Tech demo only
I did not take in style for coding this thing,
just had to wip it out as fast as I can
"""
#Carnegie Mellon 15-112 Term Project First Draft

import requests
from web3.auto import w3, Web3
w = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/[api]')) #Infura api key
from eth_account.messages import defunct_hash_message


"""
Since we cannot host a node due to internet restrictions
And we dont want each client to download the blockchain
We will use the etherscan api to facilitate transactions
Web3 will be used to encode the transactions
"""
address='0xA31439BACB1d0f5B6A71EAD727bEF620eF6643D6'
apikey=''
apiurl='http://ropsten.etherscan.io/api?'
privkey=''



"""
Gets the balance of a target account
"""
def getBalance():
    targeturl = '%smodule=account&action=balance&address=%s&tag=latest&apikey=%s' \
                % (apiurl, address, apikey)
    reply = requests.get(targeturl)
    output = reply.json()
    balance = output['result']
    readable_balance = int(balance) / 10**18
    return readable_balance



"""
Nonce is the transaction sequence
of the account, having Nonce ensures
an attacker cannot copy the transaction
hex and rebroadcast it to the network
"""
def getNonce():
    targeturl = '%smodule=proxy&action=eth_getTransactionCount&address=%s&tag=latest&apikey=%s' \
                % (apiurl, address, apikey)
    reply = requests.get(targeturl)
    output = reply.json()
    return output['result']



"""
Signs a message using the provided
private key
"""
def signMessage(msg):
    message_hash = defunct_hash_message(text=msg)
    return w3.eth.account.signHash(message_hash, private_key=privkey)



"""
Generates a raw transaction based on
the given templates and custom values
to encode
"""
def generateTransaction(dataToEncode):
    transaction = {
        'to': '0x687422eEA2cB73B5d3e242bA5456b782919AFc85',
        'value': 10 ** 11,
        'nonce': getNonce(),
        # Gas value and price stable on Ropsten
        'gas': int(4* 10 ** 6),
        'gasPrice': 10 ** 9,
        'data': str.encode(dataToEncode),
        'chainId': 3
    }
    return transaction


"""
Broadcasts the transaction onto
the Ropsten Ethereum chain
"""
def broadcastTransaction(transaction):
    signed = w.eth.account.signTransaction(transaction, privkey)
    transaction_id = w.eth.sendRawTransaction(signed.rawTransaction)
    return(transaction_id.hex())


"""
Takes in the transaction id
and returns the decoded version
"""
def decodeTransaction(transactionid):
    null = 0
    targeturl = '%smodule=proxy&action=eth_getTransactionByHash&txhash=%s&apikey=%s' % (apiurl, transactionid, apikey)
    reply = requests.get(targeturl)
    output = reply.json()
    try:
        encoded = output['result']['input']
    except:
        return "There is no data within the transaction"
    return w3.toText(encoded)


import webbrowser
def openExplorer(transactionid):
    webbrowser.open('https://ropsten.etherscan.io/tx/'+transactionid)

def basicTransaction(messages):
    transaction = generateTransaction(messages)
    result = broadcastTransaction(transaction)
    print("Txid: " + result)
    print("Open transaction within default webbrowser? [Y/N] ")
    openLink = input()
    openLink = openLink.lower()
    if openLink == 'y':
        openExplorer(result)
    else:
        pass

testmessage = "using infura api"

#Encodes test message
#basicTransaction(testmessage)
#Declaration of independence!
#print(decodeTransaction('0x24cbe2ae0b60365c1421fe7a2fc499cf8232cb0d92667ad9ec625d805e689a2f'))
