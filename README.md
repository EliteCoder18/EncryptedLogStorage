# EncryptedLogStorage
# LogPin

**Secure, encrypted log archiving using IPFS and blockchain-backed immutability.**

---

## Overview

**LogPin** is a Python-based pipeline that:

1. **Encrypts system/application logs** and saves them as PDF.
2. Uploads the encrypted PDF to **IPFS** for decentralized, permanent storage.
3. Stores the **IPFS CID (hash) on the blockchain** to ensure immutability and verifiable proof of existence.

This project is designed for research and practical applications where logs need to be:

* Securely stored
* Tamper-proof
* Decentralized and recoverable

---

##  Features

* **Encryption-first**: Logs are encrypted before upload for data privacy.
* **Decentralized storage**: Uses IPFS to store logs permanently.
* **Immutable hash storage**: Stores the IPFS CID on the blockchain for tamper-proof, verifiable logging.
* **Python-powered**: Easy to understand, modify, and extend.

---

##  Tech Stack

* **Python** (processing, encryption, IPFS upload, blockchain interaction)
* **IPFS** (via Pinata)
* **Blockchain** (Sepolia Ethereum testnet currently)
* **PDF Encryption** (`PyPDF2`, `reportlab`)

---

## Project Structure

```
LogPin/
│
├── log_encryptor.py       # Encrypts and generates PDF from logs
├── ipfs_uploader.py       # Uploads encrypted PDFs to IPFS
├── blockchain_pusher.py   # Stores CID/hash on blockchain
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## Getting Started

1 **Clone the repository:**

```bash
git clone https://github.com/yourusername/LogPin.git
cd LogPin
```

2 **Install dependencies:**

```bash
pip install -r requirements.txt
```

3 **Set up environment variables:**

Create a `.env` file:

```
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_API_KEY=your_pinata_secret
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/your_project_id
PRIVATE_KEY=your_wallet_private_key
```

4 **Run the pipeline:**

```bash
python log_encryptor.py
python ipfs_uploader.py
python blockchain_pusher.py
```

---

## 💡 Use Cases

* Secure ransomware-resistant log storage
* Forensics-ready system/application log archiving
* Decentralized log management for distributed environments
* Academic/research blockchain + IPFS data integrity projects

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests to add features, fix bugs, or improve documentation.

---

## 📜 License

MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgements

* [IPFS](https://ipfs.io/)
* [Pinata](https://pinata.cloud/)
* [web3.py](https://web3py.readthedocs.io/)
* [PyPDF2](https://pypi.org/project/PyPDF2/)
* [reportlab](https://www.reportlab.com/)

---

## 📧 Contact

If you find this project useful, consider ⭐ starring the repo.

For queries, open an issue on [GitHub](https://github.com/yourusername/LogPin/issues) or reach out at [your.email@example.com](mailto:your.email@example.com).
