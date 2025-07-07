from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import win32evtlog
from fpdf import FPDF
import os
import time
from datetime import datetime, timedelta
import zipfile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import requests
import hashlib

# === CONFIGURATION ===
server = 'localhost'
log_type = input("Enter log type (System, Application, Security): ")
max_events = 100
output_dir = "C:/Logs"
os.makedirs(output_dir, exist_ok=True)

# AES-256 key (32 bytes)
encryption_key = b'ThisIs32ByteLongSecretKeyForAES!'

# Pinata API keys (replace with your own)
PINATA_API_KEY = '74b767fe5705c9a11c9c'
PINATA_SECRET_API_KEY = '1ee9a409610cda2926f579bfbb8734b6835e73ed64f04563a8faf8ad26d82032'

def extract_logs(last_n_seconds=3000):
    logs = []
    try:
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        threshold_time = datetime.now() - timedelta(seconds=last_n_seconds)
        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                break
            for event in events:
                event_time_str = event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S")
                event_time = datetime.strptime(event_time_str, "%Y-%m-%d %H:%M:%S")
                if event_time < threshold_time:
                    win32evtlog.CloseEventLog(handle)
                    return logs
                logs.append({
                    "TimeGenerated": event_time_str,
                    "SourceName": event.SourceName,
                    "EventID": event.EventID,
                    "EventType": event.EventType,
                    "Category": event.EventCategory,
                })
        win32evtlog.CloseEventLog(handle)
    except Exception as e:
        print(f"❌ Error extracting logs: {e}")
    return logs

def save_logs_to_pdf(logs, timestamp):
    safe_timestamp = timestamp.replace(":", "_")
    pdf_filename = f"{log_type}Logs{safe_timestamp}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{log_type} Event Logs @ {timestamp}", ln=True, align='C')
    pdf.ln(10)
    for idx, log in enumerate(logs):
        pdf.multi_cell(0, 10, 
            f"{idx+1}. Time: {log['TimeGenerated']}\n"
            f"Source: {log['SourceName']}\n"
            f"Event ID: {log['EventID']} | Type: {log['EventType']} | Category: {log['Category']}\n" )
    pdf.output(pdf_path)
    return pdf_path

def compress_file(file_path):
    zip_path = file_path.replace(".pdf", ".zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))
    return zip_path

def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    iv = get_random_bytes(16)
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    encrypted_file_path = file_path.replace(".zip", ".enc")
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)
    print(f"🔐 Encrypted file saved to: {encrypted_file_path}")
    return encrypted_file_path

def upload_to_pinata(file_path):
    if not os.path.isfile(file_path):
        print("❌ Error: File not found.")
        return None
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    try:
        with open(file_path, 'rb') as file:
            filename_only = os.path.basename(file_path)
            files = {'file': (filename_only, file)}
            response = requests.post(url, files=files, headers=headers)
        if response.status_code == 200:
            ipfs_hash = response.json()['IpfsHash']
            print(f"✅ Uploaded to IPFS: https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
            return ipfs_hash
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return None

print("🔁 Starting log extraction every 30 seconds. Press Ctrl+C to stop.")

def generate_file_hash(enc_path):
    sha256_hash = hashlib.sha256()
    with open(enc_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()




try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs = extract_logs(last_n_seconds=3000)
        if logs:
            pdf_path = save_logs_to_pdf(logs, timestamp)
            zip_path = compress_file(pdf_path)
            print(f"✅ PDF saved: {pdf_path}")
            print(f"✅ Compressed: {zip_path}")
            enc_path = encrypt_file(zip_path)
            ipfs_cid = upload_to_pinata(enc_path)
            if ipfs_cid:
                print(f"🌐 CID: {ipfs_cid}")
            file_hash = generate_file_hash(enc_path)
            print("🔐 File SHA-256 hash:", file_hash)

        
        else:
            print(f"No new logs found at {timestamp}")
        time.sleep(30)
except KeyboardInterrupt:
    print("\n⛔ Stopped by user.")
