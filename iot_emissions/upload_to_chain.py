import os, json
from dotenv import load_dotenv
from web3 import Web3
from iot_emissions.mock_sensor import read_emission_data
from datetime import datetime

# Load environment from backend_sdk/.env
load_dotenv(dotenv_path="backend_sdk/.env")

# Web3 Setup
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# Load ABI
with open("backend_sdk/abi.json") as f:
    abi = json.load(f)

# Bind contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Read from sensor
emission_kg = read_emission_data()

# Log emission on-chain
print(f"[{datetime.now()}] Uploading {emission_kg} kg to smart contract...")

tx = contract.functions.logEmissions(account.address, int(emission_kg)).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 2000000,
    'gasPrice': w3.to_wei('10', 'gwei')
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=os.getenv("PRIVATE_KEY"))
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)



print(f"✅ Emission data uploaded. Tx Hash: {tx_hash.hex()}")
