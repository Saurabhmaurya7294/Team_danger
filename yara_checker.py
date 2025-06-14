# yara_checker.py
import yara

rules = yara.compile(filepath="rules.yar")

def scan_file_with_yara(file_path):
    try:
        matches = rules.match(filepath=file_path)
        return matches
    except Exception as e:
        print(f"[YARA Error] {e}")
        return []
