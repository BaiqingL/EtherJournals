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
Opens the transaction id within the default
web browser
"""
def openExplorer(transactionid):
    webbrowser.open('https://ropsten.etherscan.io/tx/'+transactionid)

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
    """
    Basic values:
    'value': 10 ** 11
    'chainId': 3
    """
    try:
        str.encode(dataToEncode)
    except:
        pass
    transaction = {
        'to': '0x687422eEA2cB73B5d3e242bA5456b782919AFc85',
        'value': 10 ** 15,
        'nonce': getNonce(),
        # Gas value and price stable on Ropsten
        'gas': int(4* 10 ** 6),
        'gasPrice': 10 ** 9,
        'data': dataToEncode,
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
    #Returns the hex id instead of the raw id for readability
    return(transaction_id.hex())

"""
Takes in the transaction id
and returns the decoded version
"""
def decodeTransaction(transactionid):
    null = 0 #Fixes entires where null is present
    targeturl = '%smodule=proxy&action=eth_getTransactionByHash&txhash=%s&apikey=%s' % (apiurl, transactionid, apikey)
    reply = requests.get(targeturl)
    output = reply.json()
    try:
        encoded = output['result']['input']
    except:
        return "There is no data within the transaction"
    #Returns bytes instead of text, allows raw data output
    return w3.toBytes(hexstr=encoded)


"""
Returns a list of all the transactions under an address
"""
def getTransactions(address):
    targeturl = '%smodule=account&action=txlist&address=%s&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=%s' \
                % (apiurl, address, apikey)
    reply = requests.get(targeturl)
    errorResponse = "This is not a valid transaction on the Ropsten network"
    try:
        output = reply.json()
    except:
        return errorResponse
    result = output['result']
    answers = []
    for entries in range(len(result)):
        answers.append(result[entries]['hash'])
    return answers

"""
Write data to file
The filename is the
txid of the data
"""
def writeDataToFile(txid, decodeddata):
    file = open(txid, "wb")
    file.write(decodeddata)
    file.close()
    print("Data written to: " + txid)

"""
Temporary method to create 
and facilitate transactions
"""
def basicTransaction(messages):
    transaction = generateTransaction(messages)
    result = broadcastTransaction(transaction)
    print("TXID: " + result)
    print("Open transaction within the default web browser? [Yes] ")
    openLink = input()
    openLink = openLink.lower()
    if openLink == 'y' or "" or "yes":
        openExplorer(result)
    print("Goodbye.")


"""
testmessage = "using infura api"
#Encodes test message, the longer the text message, the more gas it consumes from the network, 
which requires higher gas limits 
(default set to max, hence insufficient gas usage is no concern)
basicTransaction(testmessage)
"""

"""
Reads the data into jpgdata
with open('ethereum.jpg', 'rb') as inf:
    jpgdata = inf.read()
    
After encoding, decode it using:
txid = '0x9b8ffdae84d299ce111a072409df468db99fc3110fc1f928ec9b432c131cd6a5'
decoded = decodeTransaction('0x9b8ffdae84d299ce111a072409df468db99fc3110fc1f928ec9b432c131cd6a5')
writeDataToFile(txid, decoded)
"""



#Declaration of independence!
txid = '0x24cbe2ae0b60365c1421fe7a2fc499cf8232cb0d92667ad9ec625d805e689a2f'
writeDataToFile(txid, decodeTransaction(txid))

