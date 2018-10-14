#!/usr/bin/env python3
from ens import ENS
from web3 import Web3, HTTPProvider
#Using the public node infura provides, thx
w3 = Web3(HTTPProvider('https://mainnet.infura.io/'))
ns = ENS.fromWeb3(w3)

#Ensures the node is connected
assert(w3.isConnected() == True)


#Get the name and coverts it to a string if possible
def getName():
    return str(input("Enter the ENS Domain: "))


#Resolves the domain to the address
def nameToAddress():
    domain = getName()
    while not domain.endswith('.eth'):
        print("Please enter domain with '.eth'")
        domain = getName()
    print(ns.address(domain))


#Attempts to lookup the name associated with the address
def addressToName():
    address = getName()
    while not address.startswith('0x'):
        print('Enter a valid eth address: ')
        address = getName()
    try:
        print(ns.name(address))
    except:
        print("Invalid Address")
        addressToName()


def selectChoice():
    choice = input("Choose to resolve or reverse lookup\n1) Resolve\n2) Reverse Lookup\n")
    if choice == '1':
        nameToAddress()
        return
    elif choice == '2':
        addressToName()
        return
    else:
        print("Choice invalid")
        selectChoice()

selectChoice()
