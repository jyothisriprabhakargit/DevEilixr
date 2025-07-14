import os
import json
import random
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Load private key and wallet
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# Load ABI and contract address
with open(os.path.join(os.path.dirname(__file__), "abi.json")) as f:
    abi = json.load(f)

CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Function to simulate carbon offset logic
def run_carbon_agent(agent_type: str):
    if agent_type == "identity_agent":
        # Simulate emission offset event
        emission_kg = random.randint(20, 80)
        print(f"{datetime.now()} - Emission to log: {emission_kg}kg")

        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

        txn = contract.functions.logEmissions(WALLET_ADDRESS, emission_kg).build_transaction({
    "from": WALLET_ADDRESS,
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("5", "gwei")
})


        signed_tx = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ Emissions logged. Tx: {tx_hash.hex()}")

    elif agent_type == "yield_agent":
        print("🚧 Yield agent logic not yet implemented.")
        # Add future yield optimization logic here

    else:
        print(f"❌ Unknown agent type: {agent_type}")
