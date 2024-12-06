import hashlib
import os
import sys
import tkinter as tk
from tkinter import messagebox


class SecurityChecker:
    def __init__(self):
        self.critical_files = [
            os.path.join('core', 'client', 'version_checker.py'),
            os.path.join('core', 'client', 'key_system.py'),
            os.path.join('core', 'constants.py')
        ]

        self.expected_hashes = {
            'core\\client\\version_checker.py': '785e37198dabff86e5270ebe1fcc0ead',
            'core\\client\\key_system.py': '75c99c13ecbbe0a50baed7f45c8ecb75',
            'core\\constants.py': '9505ce78b9b07e659b6313ed01254818',
        }

    def calculate_file_hash(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {filepath}: {e}")
            return None

    def verify_files(self):
        root = tk.Tk()
        root.withdraw()

        for filepath in self.critical_files:
            if not os.path.exists(filepath):
                messagebox.showerror(
                    "Security Error",
                    f"Critical file missing: {filepath}\nPlease reinstall the application."
                )
                return False

            actual_hash = self.calculate_file_hash(filepath)
            expected_hash = self.expected_hashes.get(filepath.replace('/', '\\'))

            if not actual_hash or (expected_hash and actual_hash != expected_hash):
                messagebox.showerror(
                    "Security Error",
                    "Critical files have been modified. Please reinstall the application."
                )
                return False

        return True