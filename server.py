from flask import Flask
import requests
from web3 import Web3
import os

app = Flask(__name__)

@app.route("/")
def home():
    # return "Hello, World!"
    web3 = Web3(Web3.HTTPProvider(os.environ['web3']))

    account_1 = "0x45105d1B56A45c9c8A14B118264A4C20F2ad70a9"
    account_2 = "0x83aB5e1Cf8E08eEB7D2D57845d115Bb579E5D66b"

    web3.defaultAccount = web3.eth.accounts[0]

    abi = json.loads('[{"constant":false,"inputs":[],"name":"init_key","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"p_key","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"disp_key","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_key","type":"string"}],"name":"set_key","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
    address = web3.toChecksumAddress("0xf3588b383E6eee6C5569Fb6C6B94F4966AC45C9F")

    contract = web3.eth.contract(address=address, abi=abi)
    nonce = web3.eth.getTransactionCount(account_1)
    private_key1 = "4ca015685674bc28c9def202507b432b7fe7ac5c6b6911c03856fbb326b78730"
    private_key2 = "7ff8dd799991369a69fa754182c0d0a9121f4ebde54f00c074a14fe71f59d11f"

    print(contract.functions.disp_key().call())
    tx = contract.functions.set_key('----0-----').buildTransaction({
        'gas': 200000,
        'gasPrice': web3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': nonce
    })
    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key1)
    tx_result = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.fromWei(web3.eth.get_balance(account_1), 'ether'))
    print(contract.functions.disp_key().call())
    
if __name__ == "__main__":
    app.run(debug=True)