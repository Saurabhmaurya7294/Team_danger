# behavior_monitor.py
import psutil

def detect_suspicious_processes():
    flagged = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if any(term in name for term in ['keylogger', 'ransom', 'stealer']):
                flagged.append(proc.info)
        except:
            continue
    return flagged
