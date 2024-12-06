import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()


class VersionChecker:
    def __init__(self, project_type="user"):
        self.project_type = project_type
        self.version_url = "https://raw.githubusercontent.com/xurst/shibrazy-macro-private/main/version.json"
        self.current_version = "1.0.0"
        self.github_token = os.getenv('GITHUB_TOKEN')

    def check_update(self):
        if self.project_type == "dev":
            return True

        try:
            headers = {
                "Authorization": f"token {self.github_token}"
            }
            response = requests.get(self.version_url, headers=headers)

            if response.status_code == 200:
                version_data = response.json()
                repo_version = version_data.get("version")

                if repo_version != self.current_version:
                    root = tk.Tk()
                    root.withdraw()

                    if self.project_type == "personal":
                        if messagebox.askyesno(
                                "Update Available",
                                "A new version is available. Would you like to update? (Your configurations will be preserved)"
                        ):
                            return False
                        return True

                    if version_data.get("required", False):
                        messagebox.showerror(
                            "Update Required",
                            "A new version is available. Please update to continue using."
                        )
                        return False

                    if messagebox.askyesno(
                            "Update Available",
                            "A new version is available. Would you like to update?"
                    ):
                        return False

            return True

        except Exception as e:
            print(f"Error checking version: {e}")
            return True