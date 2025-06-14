# virus_total_checker.py
import requests, hashlib

API_KEY = 'YOUR_VIRUSTOTAL_API_KEY'

def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_virustotal(file_path):
    file_hash = get_file_hash(file_path)
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None
