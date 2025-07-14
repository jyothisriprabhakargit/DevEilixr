# Deploy contract script placeholderfrom web3 import Web3
from solcx import compile_standard, install_solc
import json, os
from dotenv import load_dotenv
from web3 import Web3


# Load secrets
load_dotenv()

# Install correct Solidity version
install_solc("0.8.0")

# Setup Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

# Read smart contract
with open("contracts/CarbonOffsetAgent.sol", "r") as file:
    source_code = file.read()

# Compile
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"CarbonOffsetAgent.sol": {"content": source_code}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "evm.bytecode"]}
        }
    }
}, solc_version="0.8.0")

# Extract ABI & bytecode
abi = compiled_sol['contracts']['CarbonOffsetAgent.sol']['CarbonOffsetAgent']['abi']
bytecode = compiled_sol['contracts']['CarbonOffsetAgent.sol']['CarbonOffsetAgent']['evm']['bytecode']['object']

# Deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account.address)

transaction = contract.constructor().build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 3000000,
    'gasPrice': w3.to_wei('10', 'gwei')
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=os.getenv("PRIVATE_KEY"))
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)


print(f"⏳ Deploying... Tx hash: {tx_hash.hex()}")

# Wait for receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")

# Save ABI
with open("backend_sdk/abi.json", "w") as f:
    json.dump(abi, f)

# Save contract address to .env
with open("backend_sdk/.env", "a") as f:
    f.write(f"\nCONTRACT_ADDRESS={tx_receipt.contractAddress}")
