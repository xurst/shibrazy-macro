import sys
import time
import keyboard
import threading
import subprocess
from core.constants import *
from functions.client.browser.browser_handler import BrowserHandler
from functions.client.discord.discord_handler import DiscordHandler
from functions.client.checks import MessageChecker
from functions.client.emulator import EmulatorHandler
from core.client.key_system import KeySystem

class MainRunner:
    def __init__(self):
        self.running = True
        self.bot_enabled = True
        self.toggle_event = threading.Event()
        self.discord_handler = DiscordHandler()
        self.emulator = EmulatorHandler()
        self.browser_handler = BrowserHandler(self.emulator)
        self.message_checker = MessageChecker()

    def toggle_bot(self):
        try:
            last_toggle_time = 0
            while not self.toggle_event.is_set():
                current_time = time.time()
                if keyboard.is_pressed(TOGGLE_HOTKEY) and (current_time - last_toggle_time) > 0.5:
                    self.bot_enabled = not self.bot_enabled
                    status = "ENABLED" if self.bot_enabled else "DISABLED"
                    print(f"\nBot functionality {status}")
                    last_toggle_time = current_time
                    while keyboard.is_pressed(TOGGLE_HOTKEY):
                        time.sleep(0.1)
                time.sleep(0.1)
        except Exception as e:
            print(f"Error in toggle thread: {e}")

    def run(self):
        print("\n=== Discord Message Monitor ===")

        print("\nMonitored Channels:")
        for server_id, server_config in SERVER_CONFIGS.items():
            print(f"\nServer ID: {server_id}")
            for channel_id, channel in server_config['channels'].items():
                channel_name = channel.get('name', f'Channel {channel_id}')
                print(f"  • {channel_name}:")
                print(f"    - Whitelisted Keywords: {', '.join(channel['whitelist']['keywords'])}")
                print(f"    - Blacklisted Keywords: {', '.join(channel['blacklist']['keywords'])}")
                print(f"    - Match Mode: {'Any keyword' if channel['whitelist']['match_any'] else 'All keywords'}")
                webhook_mode = 'Keywords only' if channel.get('webhook_only_keywords', False) else 'All messages'
                print(f"    - Webhook Mode: {webhook_mode}")

        print("\nControls:")
        print(f"• {TOGGLE_HOTKEY} - Toggle bot")
        print(f"• Printing Mode: {'Whitelisted only' if PRINT_WHITELISTED_ONLY else 'All messages'}")
        print(f"• Print When Disabled: {'Yes' if PRINT_WHEN_DISABLED else 'No'}")
        print("\nBot is running...\n")
        print("-" * 50)

        toggle_thread = threading.Thread(target=self.toggle_bot, daemon=True)
        toggle_thread.start()

        last_message_ids = {}
        while self.running:
            try:
                for server_id, server_config in SERVER_CONFIGS.items():
                    for channel_id in server_config['channels'].keys():
                        msg = self.discord_handler.get_latest_message(channel_id)
                        if msg and msg.get('id') != last_message_ids.get(channel_id):
                            self.message_checker.process_message(
                                msg,
                                self.browser_handler,
                                server_id,
                                channel_id,
                                server_config['channels'][channel_id],
                                self.bot_enabled,
                                self.discord_handler
                            )
                            last_message_ids[channel_id] = msg.get('id')

                time.sleep(CHECK_DELAY)
            except Exception as e:
                time.sleep(RATE_LIMIT_DELAY)
                print(f"Rate limited, waiting... ({str(e)})")

    def __del__(self):
        print("\nCleaning up...")
        self.running = False
        if hasattr(self, 'toggle_event'):
            self.toggle_event.set()


def validate_license():
    key_system = KeySystem()
    max_attempts = 3
    attempts = 0

    # Check for saved key first
    saved_key = key_system.load_saved_key()
    if saved_key:
        print("\n=== License Validation ===")
        print("Found saved license key...")
        valid, message = key_system.validate_key(saved_key, check_saved=True)
        if valid:
            print(f"\n✅ {message}")
            return True
        else:
            print(f"❌ {message}")

    while attempts < max_attempts:
        print("\n=== License Validation ===")
        key = input("Please enter your license key: ").strip()

        valid, message = key_system.validate_key(key)
        if valid:
            print(f"\n✅ {message}")
            return True

        attempts += 1
        remaining = max_attempts - attempts
        print(f"\n❌ {message}")
        if remaining > 0:
            print(f"You have {remaining} attempts remaining.")

    print("\n❌ Maximum attempts reached. Please obtain a valid license key.")
    return False


if __name__ == "__main__":
    if SEPARATE_TERMINAL:
        if not sys.argv[-1] == "CHILD_PROCESS":
            python_exe = sys.executable
            script_path = os.path.abspath(__file__)
            cmd = ['cmd', '/c', 'start', 'cmd', '/k', python_exe, script_path, 'CHILD_PROCESS']
            subprocess.run(cmd)
            sys.exit()

    # Validate license before running
    if validate_license():
        runner = MainRunner()
        runner.run()
    else:
        input("\nPress Enter to exit...")
        sys.exit(1)