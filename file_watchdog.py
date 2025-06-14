# file_watchdog.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class RansomwareWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.locked') or event.src_path.endswith('.enc'):
            print(f"[ALERT] Suspicious file: {event.src_path}")

def start_watch(path='.'):
    observer = Observer()
    observer.schedule(RansomwareWatcher(), path, recursive=True)
    observer.start()
    print("[INFO] Watching for suspicious file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
