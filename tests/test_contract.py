import os
from web3 import Web3
import json
from dotenv import load_dotenv

def test_contract_connection():
    load_dotenv()
    w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
    assert w3.is_connected(), "Web3 not connected"

    with open("backend_sdk/abi.json") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=abi)
    emissions, credits = contract.functions.getStatus(os.getenv("WALLET_ADDRESS")).call()

    assert isinstance(emissions, int), "Emissions not integer"
    assert isinstance(credits, int), "Credits not integer"
