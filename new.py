import sys
import requests
import hashlib
import json
import datetime
import codecs
import os
from pycoin import ecdsa, key, encoding
from pycoin.ecdsa.secp256k1 import secp256k1_generator
from pycoin.key import Key


min_adress = '3MgUw7WaAq3EfMtospqDuKXRF9QHjaPAzs'
txid = '9b489e70aa37dcd1ba3116dccbe5c0b7b90777f56a783a9791bee4cf9b6a6c01'

rpc_user = 'jens'
rpc_pass = 'madsen'

url = 'http://%s:%s@localhost:8332' % (rpc_user, rpc_pass)
headers = {'content-type': 'application/json'}

def getSendFromAddress():
    address = input("Ange adress att skicka ifrån: ")
    return address

def getSendToAddress():
    address = input("Ange adress att skicka till: ")
    return address

def getAmount():
    amount = input("Ange belopp: ")
    return amount

def getChangeAddress():
    change_address = input("Ange växeladress: ")
    return change_address

def getFee():
    fee = input("Ange fee per kB: ")
    return fee 

def unlockWallet():
    payload = {
        "method": "walletpassphrase",
        "params": ['madsen123', 600]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

def createRawTransaction():
    transaction = [{
      "txid": txid,
      "vout" : 1
    }] 
    address_and_amount = { "3MgUw7WaAq3EfMtospqDuKXRF9QHjaPAzs": 0.01 }
    payload = {
        "method": "createrawtransaction",
        "params": [transaction, address_and_amount]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response['result']


def signRawTransaction(raw_transaction_hex):
    payload = {
        "method": "signrawtransaction",
        "params": [raw_transaction_hex]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def sendRawTransaction(hex_to_send):
    payload = {
        "method": "sendrawtransaction",
        "params": [hex_to_send]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    print(response)

def fundRawTransaction(hex_to_fund, change_address, fee):
    send_object = {
        "changeAddress" : change_address,
        "feeRate": fee
    }
    payload = {
        "method": "fundrawtransaction",
        "params": [hex_to_fund, send_object]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response

def generate_key():
    generator = secp256k1_generator
    rand = codecs.encode(os.urandom(32), 'hex').decode()
    secret_exponent = int('0x'+rand, 0)
    key = Key(secret_exponent=secret_exponent, generator=generator)
    print(key.wif())                    #wif-format
    print(key.sec_as_hex())             #hex-format
    print(key.address())                #btc-address uncompressed
    print(key.public_copy())            #public key uncompressed
    key._prefer_uncompressed = False
    print(key.address())                #btc-address compressed
    print(key.public_copy())            #public key compressed
    print(secret_exponent)              #for reuse purpose
    return key

def send_btc_menu(key1, key2):

    #send_from_address = getSendFromAddress()
    #send_to_address = getSendToAddress()
    send_from_adress = key1.address()
    send_to_address = key2.address()
    amount = getAmount()
    change_address = getChangeAddress()
    fee = getFee()

    raw_transaction_hex = createRawTransaction()
    funded_transaction = fundRawTransaction(raw_transaction_hex, change_address, fee)
    signed_transaction = signRawTransaction(funded_transaction['result']['hex'])
    print(signed_transaction)


def main():
    key1 = generate_key()
    key2 = generate_key()
    send_btc_menu(key1, key2)





    

main()

