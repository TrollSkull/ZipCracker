import sys
import os

ALLOWED_EXTENSIONS = (".zip", ".rar", ".7z")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def format_bytes(input_bytes):
    units, byte = ['bytes', 'KB', 'MB', 'GB'], 0

    while input_bytes >= 1024 and byte < len(units)-1:
        input_bytes /= 1024
        byte += 1

    return f"{input_bytes:.2f} {units[byte]}"
