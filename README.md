# Agentic Ethereum Hackathon India

# 🛠 Project Title - Carbon Offset Agent SDK 
# Team Name - DevElixir
# Team Members - Jyothisri Prabhakar , Balagajaraj Prabhakar.

Welcome to our submission for the Agentic Ethereum Hackathon by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: “Designing an AI-integrated Ethereum Agent to Automate Real-World Use Cases”  
With climate change becoming critical, industries must manage their carbon emissions efficiently. But carbon tracking is often delayed, manual, and lacks transparency. There's a need for a solution that automates carbon footprint tracking, forecasting, and offsetting — powered by blockchain for accountability.

---

## 💡 Our Solution

Project Name: *CarbonOffsetAgentSDK*  
A smart SDK + dashboard that helps companies track, predict, and offset their carbon emissions using AI + Ethereum.  

- Companies log their CO₂ emissions.
- An AI model predicts future emissions based on real-time operational data (temperature, energy, usage).
- An Ethereum Agent automates offset transactions — either using carbon credits or ETH-based payments.
- The entire lifecycle is transparent and auditable on-chain.

Our tool empowers industries, regulators, and even students to plug and play carbon intelligence into any workflow.

---

## 🧱 Tech Stack

- 🖥 Frontend: *Streamlit*
- ⚙ Backend: *Python (FastAPI-compatible structure)*
- 🧠 AI: *scikit-learn (Linear Regression model)*
- 🔗 Blockchain: *Ethereum (Solidity + Web3.py)*
- 🔍 DB/Storage: *Blockchain state + local AI model (.pkl)*
- 🚀 Hosting: *Local Deployment (Streamlit / CLI SDK)*

---
## 📂 Repository Structure

```bash
.
├── ui/                     # Streamlit UI dashboard
│   └── dashboard.py
├── backend_sdk/           # Agent logic, model loading, contract interaction
│   ├── run_agent.py
│   ├── deploy_contract.py
│   ├── abi.json
│   └── .env                # Contains RPC_URL, PRIVATE_KEY, etc.
├── ai_module/             # Emission prediction logic
│   ├── emission_prediction.py
│   └── emission_model.pkl
├── sdk_cli/               # Typer CLI agent runner
│   └── cli.py
├── contracts/             # Smart contract (Solidity)
│   └── CarbonOffsetAgent.sol
├── README.md              # A detailed description of your project
├── requirements.txt
