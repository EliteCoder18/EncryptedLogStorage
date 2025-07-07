import os
import time
import hashlib
import requests
import inspect_patch
from web3 import Web3
from dotenv import load_dotenv

#Load .env
load_dotenv("web.env")

# Setup Web3
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
ACCOUNT_ADDRESS = Web3.to_checksum_address(os.getenv("ACCOUNT_ADDRESS"))
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise Exception("Web3 is not connected. Check your RPC URL.")

#Correct ABI (must match deployed contract)
abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "ipfsCid", "type": "string"},
            {"internalType": "string", "name": "hash", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "storeLog",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalLogs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getLog",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Now initialize contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

#Upload encrypted file to Pinata IPFS
def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()["IpfsHash"]

# Generate SHA-256 hash
def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

#  Loop: Every 30 seconds
while True:
    try:
        log_path = "C:\Logs\APPLICATIONLOGS.enc"  #Your file path

        cid = upload_to_pinata(log_path)
        log_hash = get_file_hash(log_path)
        timestamp = int(time.time())

        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn = contract.functions.storeLog(cid, log_hash, timestamp).build_transaction({
            "from": ACCOUNT_ADDRESS,
            "gas": 300000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": nonce
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"[+] Log Stored | CID: {cid} | Hash: {log_hash} | Timestamp: {timestamp}")
        print(f"    Tx Hash: {w3.to_hex(tx_hash)}\n")

    except Exception as e:
        print(f"[!] Error: {str(e)}")

    time.sleep(30)
