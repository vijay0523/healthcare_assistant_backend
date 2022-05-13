import json
from web3 import Web3
from solc import compile_source, compile_files, install_solc

#install_solc('v0.4.20')
compiled_sol = compile_files(['./contract.sol'])
print(compiled_sol.keys())

# Compiled solidity code
contract_interface = compiled_sol['./contract.sol:Key']


# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://192.168.56.102:7545"))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
#print(contract)
abi=contract_interface['abi']
ganache_url = "http://192.168.56.102:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))

account_create = web3.eth.account.create()
account_1 = "0x339C60fF204Bc17fC6Ed24aaE31a185A2b47725C"
account_2 = "0xeFc822E4f9669d8161878F4652a8b174145F0852"

#print(account_1)
print(web3.fromWei(web3.eth.get_balance(account_1), 'ether'))
#print(web3.eth.get_accounts())
#print(len(web3.eth.get_accounts()))
#web3.defaultAccount = web3.eth.accounts[0]

#contract = web3.eth.contract(address=address, abi=abi)
nonce = web3.eth.getTransactionCount(account_1)
private_key1 = "dd6e819a2c6b9136d90aadabadaaad0f4050d383846aaeb9f39b074632982832"
private_key2 = "9e873a08f2c60d461dbf9a95f2189ad31abf5e1249c977d18ba32600e983f565"

tx = contract.constructor().buildTransaction({
	'gas': 400000,
	'gasPrice': web3.toWei('1000', 'gwei'),
	'from': account_1,
	'nonce': nonce
})
signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key1)
tx_result = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

#tx_hash = contract.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_result)
print("Smart Contract Created '%s'" % tx_receipt.contractAddress)

contract = web3.eth.contract(
	address=tx_receipt.contractAddress,
	abi=abi
)

nonce = web3.eth.getTransactionCount(account_1)
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


