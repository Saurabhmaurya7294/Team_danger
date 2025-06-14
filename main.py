# main.py
from virus_total_checker import check_virustotal
from yara_checker import scan_file_with_yara
from behavior_monitor import detect_suspicious_processes
from file_watchdog import start_watch
import sys

def scan_file(file_path):
    print(f"\n🔍 Scanning: {file_path}")

    print("\n[1] VirusTotal Scan...")
    vt = check_virustotal(file_path)
    if vt:
        stats = vt['data']['attributes']['last_analysis_stats']
        print(f"VirusTotal: {stats}")
        if stats['malicious'] > 0:
            print("⚠️ File flagged as malicious!")
    else:
        print("❌ Could not scan with VirusTotal.")

    print("\n[2] YARA Rule Check...")
    matches = scan_file_with_yara(file_path)
    if matches:
        print("⚠️ YARA match found!")
        for match in matches:
            print(f"- {match.rule}")
    else:
        print("✅ No YARA rule matched.")

    print("\n[3] Suspicious Processes Check...")
    suspicious = detect_suspicious_processes()
    if suspicious:
        print("⚠️ Suspicious processes running:")
        for proc in suspicious:
            print(proc)
    else:
        print("✅ No suspicious processes detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_to_scan>")
        print("Or run: python main.py watch   ← starts ransomware file monitoring")
    elif sys.argv[1] == 'watch':
        start_watch()
    else:
        scan_file(sys.argv[1])
