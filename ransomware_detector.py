import os
import psutil
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv
from openpyxl import Workbook

# --------------------- Configuration ---------------------
SUSPICIOUS_EXTENSIONS = {'.locked', '.enc', '.crypt', '.crypto', '.ransom'}
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_CSV = os.path.join(LOGS_DIR, "ransomware_scan_log.csv")
LOG_FILE_XLSX = os.path.join(LOGS_DIR, "ransomware_scan_log.xlsx")


# --------------------- Ransomware Monitor Class ---------------------
class RansomwareMonitor(FileSystemEventHandler):
    def __init__(self, log_widget):
        self.log_widget = log_widget
        self.create_log()

    def create_log(self):
        if not os.path.exists(LOG_FILE_CSV):
            with open(LOG_FILE_CSV, mode='w', newline='', encoding='utf-8') as log_file:
                writer = csv.writer(log_file)
                writer.writerow(["Timestamp", "Message", "Tag"])

    def on_modified(self, event):
        if not event.is_directory:
            _, ext = os.path.splitext(event.src_path)
            if ext in SUSPICIOUS_EXTENSIONS:
                log_message = f"\u26A0 Suspicious File Detected: {event.src_path}"
                self.log_event(log_message, "high")
                block_ransomware()
            else:
                log_message = f"\u2705 Non-Suspicious File Detected: {event.src_path}"
                self.log_event(log_message, "low")

    def log_event(self, message, tag):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"{timestamp} - {message}"

        with open(LOG_FILE_CSV, mode='a', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([timestamp, message, tag])

        self.log_widget.insert(tk.END, full_message + "\n", tag)
        self.log_widget.yview(tk.END)

    def scan_system(self):
        directories_to_scan = [os.path.expanduser("~"), "C:/", "/home/"]

        for directory in directories_to_scan:
            self.log_event(f"Scanning directory: {directory}", "info")
            for root, dirs, files in os.walk(directory):
                for file in files:
                    _, ext = os.path.splitext(file)
                    file_path = os.path.join(root, file)
                    if ext in SUSPICIOUS_EXTENSIONS:
                        self.log_event(f"Suspicious file found: {file_path}", "high")
                        block_ransomware()
                    else:
                        self.log_event(f"Non-suspicious file: {file_path}", "low")
            self.log_event(f"Finished scanning {directory}\n", "info")


# --------------------- Ransomware Blocker ---------------------
def block_ransomware():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if any(word in proc.info['name'].lower() for word in ["ransom", "encrypt", "locker"]):
                psutil.Process(proc.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# --------------------- Monitoring Function ---------------------
def start_monitoring(log_widget):
    observer = Observer()
    event_handler = RansomwareMonitor(log_widget)
    observer.schedule(event_handler, path=os.path.expanduser("~"), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# --------------------- Scan Trigger ---------------------
def start_scan(log_widget):
    monitor = RansomwareMonitor(log_widget)
    threading.Thread(target=monitor.scan_system, daemon=True).start()


# --------------------- GUI ---------------------
def start_gui():
    root = tk.Tk()
    root.title("Ransomware Detection System")
    root.geometry("800x600")
    root.configure(bg="#1e1e1e")

    label = tk.Label(root, text="\u2692 Ransomware Monitor", font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e")
    label.pack(pady=10)

    log_widget = scrolledtext.ScrolledText(root, height=20, width=100, bg="#121212", fg="white", font=("Consolas", 10))
    log_widget.pack(pady=10)
    log_widget.tag_config("high", foreground="red")
    log_widget.tag_config("low", foreground="green")
    log_widget.tag_config("info", foreground="cyan")

    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Start System Scan", command=lambda: start_scan(log_widget),
              bg="#4dff4d", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(button_frame, text="Force Kill Malware", command=block_ransomware,
              bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(button_frame, text="View Log", command=lambda: os.system(f'notepad.exe {LOG_FILE_CSV}'),
              bg="#ffcc00", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=5, pady=5)

    threading.Thread(target=start_monitoring, args=(log_widget,), daemon=True).start()

    root.mainloop()


# --------------------- Entry Point ---------------------
if __name__ == "__main__":
    start_gui()
