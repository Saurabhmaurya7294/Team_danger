import requests
import os
from dotenv import load_dotenv

load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_BASE_URL = "https://api.pinata.cloud/"
PIN_FILE_URL = PINATA_BASE_URL + "pinning/pinFileToIPFS"

HEADERS = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_API_KEY
}

def upload_to_pinata(filepath):
    with open(filepath, 'rb') as f:
        response = requests.post(PIN_FILE_URL, files={"file": f}, headers=HEADERS)
    return response.json()