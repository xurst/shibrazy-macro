import os
import json
import uuid
import requests
import pymongo
import subprocess
from datetime import datetime


class KeySystem:
    def __init__(self):
        self.api_endpoint = "https://af2a6f23-8ec4-44a6-acc8-925eb377c951-00-2nq6jqze400ra.picard.replit.dev/validate"
        self.save_file = 'saved_key.json'

    def get_hwid(self):
        """Get unique hardware ID"""
        try:
            system_uuid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip()
            disk_serial = str(subprocess.check_output('wmic diskdrive get serialnumber')).split('\\r\\n')[1].strip()
            cpu_id = str(subprocess.check_output('wmic cpu get processorid')).split('\\r\\n')[1].strip()
            combined = f"{system_uuid}-{disk_serial}-{cpu_id}"
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, combined))
        except:
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode())))

    def validate_key(self, key, check_saved=False):
        """Check if a key is valid and unused"""
        if not key or not isinstance(key, str) or not key.startswith("KEY_"):
            return False, "Invalid key format. Key must start with 'KEY_'"

        try:
            current_hwid = self.get_hwid()

            # First, check with the server about existing keys for this HWID
            response = requests.post(
                self.api_endpoint,
                json={
                    'key': key,
                    'hwid': current_hwid,
                    'check_only': True  # New parameter to just check without validating
                },
                headers={
                    'Content-Type': 'application/json'
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                existing_key = data.get('existing_key')

                # If there's an existing different key and this isn't a saved key check
                if existing_key and existing_key != key and not check_saved:
                    print(f"\nWarning: You already have a key ({existing_key}) registered on this hardware.")
                    while True:
                        choice = input("Do you want to use the new key instead? (y/n): ").lower().strip()
                        if choice in ['y', 'n']:
                            if choice == 'n':
                                self.save_key(existing_key)
                                return True, "Using existing key"
                            break
                        print("Please enter 'y' or 'n'")

                # Only proceed with validation if we don't have an existing key
                # or if the user chose to use the new key
                validation_response = requests.post(
                    self.api_endpoint,
                    json={
                        'key': key,
                        'hwid': current_hwid,
                        'force_new': True  # Add force_new flag when user chooses new key
                    },
                    headers={
                        'Content-Type': 'application/json'
                    },
                    timeout=10
                )

                if validation_response.status_code == 200:
                    validation_data = validation_response.json()
                    if validation_data.get('valid'):
                        self.save_key(key)
                        return True, validation_data.get('message', 'Key validated successfully')
                    return False, validation_data.get('message', 'Invalid key')

            return False, "Error connecting to validation server"

        except requests.exceptions.Timeout:
            return False, "Validation server timeout - please try again"
        except requests.exceptions.ConnectionError:
            return False, "Could not connect to validation server"
        except Exception as e:
            return False, f"Error validating key: {str(e)}"

    def save_key(self, key):
        """Save a validated key to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump({
                    'key': key,
                    'hwid': self.get_hwid()
                }, f)
        except Exception as e:
            print(f"Warning: Could not save key - {e}")

    def load_saved_key(self):
        """Load a previously saved key"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    if data.get('hwid') == self.get_hwid():
                        return data.get('key')
        except Exception as e:
            print(f"Warning: Could not load saved key - {e}")
        return None