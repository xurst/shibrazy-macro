#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
from core.constants import *  # opy: preserve import
from core.client.key_system import KeySystem  # opy: preserve import

REPLIT_API = "https://af2a6f23-8ec4-44a6-acc8-925eb377c951-00-2nq6jqze400ra.picard.replit.dev"

class DiscordBot(object):  # opy: not rename
    def __init__(self):
        self.key_system = KeySystem()

    def start_background(self):  # opy: not rename
        """No-op function to maintain compatibility"""
        pass

if __name__ == "__main__":  # opy: not rename
    if SEPARATE_TERMINAL:
        if not sys.argv[-1] == "CHILD_PROCESS":
            python_exe = sys.executable
            script_path = os.path.abspath(__file__)
            cmd = ['cmd', '/c', 'start', 'cmd', '/k', python_exe, script_path, 'CHILD_PROCESS']
            subprocess.run(cmd)
            sys.exit()

    print("\n=== Bot Starting ===")
    discord_bot = DiscordBot()