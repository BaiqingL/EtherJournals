#!/usr/bin/env python3

from web3 import Web3
local_provider = Web3.IPCProvider('directory/geth.ipc')
w3 = Web3(local_provider)
assert(w3.isConnected() == True)
print("Connected to the local geth node!\n")
print(w3.eth.getBlock("latest"))
blockNumber = w3.eth.getBlock("latest")['number']
if blockNumber == 0: print("\nGeth not synced\n")
print(w3.eth.syncing)
