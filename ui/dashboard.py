import streamlit as st
from web3 import Web3
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import pickle
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Import prediction module
from ai_module.emissions_predictor import predict_emission

# Load environment variables
load_dotenv(dotenv_path=os.path.join("backend_sdk", ".env"))

# Streamlit UI setup
st.set_page_config(page_title="Carbon Offset Agent", layout="centered")
st.title("🌱 Carbon Offset Dashboard")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# Load contract ABI
with open("backend_sdk/abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# Get user input for wallet
user_address = st.text_input("🔎 Enter Wallet Address", account.address)

# Store last transaction
if "last_tx" not in st.session_state:
    st.session_state.last_tx = None

# -------------------------
# Emission Status Check
# -------------------------
if st.button("📊 Get Emission Status"):
    emissions, credits = contract.functions.getStatus(user_address).call()
    st.success(f"🔴 Emissions: {emissions} kg")
    st.success(f"🟢 Carbon Credits: {credits} kg")


if st.button("✅ Offset Now"):

    emissions, _ = contract.functions.getStatus(user_address).call()

    if emissions == 0:
        st.success("✅ No emissions to offset.")
    else:
        eth_per_kg = 0.00001
        total_eth = emissions * eth_per_kg
        st.info(f"Predicted Emission: {emissions:.2f} kg CO₂")
        st.info(f"💸 Estimated Offset Cost: {total_eth:.6f} ETH")

    # Get current nonce
    nonce = w3.eth.get_transaction_count(account.address)

    # Payment Transaction
    offset_wallet = "0xaD27BDXXXXXXXXXXXXXXXXXXXXXX"
    payment_tx = {
        'from': account.address,
        'to': Web3.to_checksum_address(offset_wallet),
        'value': Web3.to_wei(total_eth, 'ether'),
        'gas': 21000,
        'gasPrice': int(w3.eth.gas_price * 1.1),
        'nonce': nonce,
        'chainId': 11155111
    }

    signed_payment_tx = w3.eth.account.sign_transaction(payment_tx, account.key)
    payment_tx_hash = w3.eth.send_raw_transaction(signed_payment_tx.rawTransaction)
    st.success(f"✅ Payment Sent: {payment_tx_hash.hex()}")

    # Smart Contract: Call offset() to reset emissions
# Prepare transaction to call payToOffset()
    offset_txn = contract.functions.payToOffset().build_transaction({
    'from': account.address,
    'value': Web3.to_wei(total_eth, 'ether'),
    'gas': 200000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': w3.eth.get_transaction_count(account.address),
    'chainId': 11155111
})

    signed_offset_tx = w3.eth.account.sign_transaction(offset_txn, account.key)
    offset_tx_hash = w3.eth.send_raw_transaction(signed_offset_tx.rawTransaction)
    st.success(f"✅ Emission Reset Done:\n{offset_tx_hash.hex()}")

    st.session_state.last_tx = offset_tx_hash.hex()

# -------------------------
# Show Last Transaction
# -------------------------
if st.session_state.last_tx:
    st.info(f"📌 Last Transaction: {st.session_state.last_tx}")
    st.markdown(f"[🔗 View on Explorer](https://sepolia.etherscan.io/tx/{st.session_state.last_tx})")

# -------------------------
# AI Prediction UI
# -------------------------
st.markdown("---")
st.subheader("🤖 AI-Based Emission Forecast")

col1, col2, col3 = st.columns(3)
with col1:
    temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, value=27.0)
with col2:
    energy = st.number_input("⚡ Energy Consumed (kWh)", min_value=0.0, value=55.0)
with col3:
    machine_hours = st.number_input("🛠️ Machine Hours", min_value=0.0, value=8.5)

if st.button("🧠 Predict Emission"):
    model_path = "ai_module/emission_model.pkl"
    if not os.path.exists(model_path):
        st.error("⚠️ AI Model not trained. Please train it first.")
    else:
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        features = [temp, energy, machine_hours]
        st.session_state["features"] = features

        prediction = model.predict([features])[0]
        st.session_state["prediction"] = prediction

        st.success(f"📈 Predicted Emissions: **{prediction:.2f} kg CO₂**")

        if prediction < 10:
            st.success("✅ Emissions are low. Keep up the efficient operations!")
        elif 10 <= prediction < 12:
            st.warning("⚠️ Moderate emissions. Consider small optimizations.")
        else:
            st.error("🚨 High emissions! Take action.")
            st.markdown("**Suggestions:**")
            st.markdown("- Reduce machine runtime during peak temperature hours")
            st.markdown("- Shift to renewable energy sources")
            st.markdown("- Schedule predictive maintenance")

        st.caption(f"🕒 Prediction generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# -------------------------
# Offset Now
# -------------------------
