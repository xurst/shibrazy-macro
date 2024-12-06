import re
from core.constants import *
from fuzzywuzzy import fuzz
import logging
import pygame

logger = logging.getLogger('message_checker')

class MessageChecker:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(SOUND_VOLUME)
        self.load_sound_files()

    def load_sound_files(self):
        self.sound_files = []
        if PLAY_SOUND and os.path.exists(SOUND_DIR):
            for file in os.listdir(SOUND_DIR):
                if file.endswith('.mp3'):
                    self.sound_files.append(os.path.join(SOUND_DIR, file))

    def play_notification_sound(self):
        if PLAY_SOUND and self.sound_files:
            try:
                sound_file = self.sound_files[0]  # Use the first sound file
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.set_volume(SOUND_VOLUME)  # Ensure volume is set before playing
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing sound: {e}")

    def check_keywords(self, content, keyword_config, match_any, is_blacklist=False):
        content_lower = content.lower()
        keywords_found = []

        match_ratio = BLACKLIST_MATCH_RATIO if is_blacklist else WHITELIST_MATCH_RATIO

        for keyword in keyword_config["keywords"]:
            for word in content_lower.split():
                ratio = fuzz.ratio(word.lower(), keyword.lower())
                if ratio >= match_ratio:
                    keywords_found.append(keyword)
                    break

        return any(keywords_found) if match_any else len(keywords_found) == len(
            keyword_config["keywords"]), keywords_found

    def extract_roblox_url(self, content):
        if "https://www.roblox.com/share?code=" in content:
            match = re.search(r"https://www\.roblox\.com/share\?code=\S+", content)
            if match:
                return match.group(0).strip()
        return None

    def process_message(self, msg, browser_handler, server_id, channel_id, channel_config, bot_enabled=True,
                        discord_handler=None):
        if not msg or not channel_config:
            return

        content = msg.get('content', '')
        whitelist_match, whitelist_found = self.check_keywords(content, channel_config['whitelist'],
                                                               channel_config['whitelist']['match_any'],
                                                               is_blacklist=False)
        blacklist_match, blacklist_found = self.check_keywords(content, channel_config['blacklist'],
                                                               channel_config['blacklist']['match_any'],
                                                               is_blacklist=True)

        url = self.extract_roblox_url(content)

        if bot_enabled:
            if url and whitelist_match and not blacklist_match and ACTUAL_JOINING:
                print(f"\nFound a link: {url}")
                if whitelist_found:
                    print(f"Matched keywords: {whitelist_found}")
                    self.play_notification_sound()  # Play sound when keywords are found
                browser_handler.open_url(url)
            elif url and whitelist_match and not blacklist_match and not ACTUAL_JOINING:
                print(f"\nFound a link but ACTUAL_JOINING is disabled (debug mode): {url}")
                print(f"Matched keywords: {whitelist_found}")
                self.play_notification_sound()  # Play sound when keywords are found
            elif url and blacklist_match:
                print(f"\nBlacklisted keywords found: {blacklist_found}")

        # Determine if we should process output (terminal and webhook)
        should_process = False
        if bot_enabled or PRINT_WHEN_DISABLED:
            if PRINT_WHITELISTED_ONLY:
                should_process = whitelist_match and not blacklist_match
            else:
                should_process = True

        # Handle webhook messages based on should_process
        if should_process and WEBHOOKING and discord_handler and not blacklist_match:
            if PRINT_WHITELISTED_ONLY:
                if whitelist_match:
                    discord_handler.send_webhook_message(channel_config['name'], msg, whitelist_found)
            else:
                discord_handler.send_webhook_message(channel_config['name'], msg,
                                                     whitelist_found if whitelist_match else None)

        # Handle terminal output based on should_process
        if should_process:
            author = msg.get('author', {})
            username = author.get('username', 'Unknown')
            user_id = author.get('id', 'Unknown')
            server_name = SERVER_CONFIGS[server_id]["name"]
            channel_name = channel_config["name"]

            print(f"\nNew Message in {server_name}, Channel: {channel_name}:")
            print(f"User: {username} ({user_id})")
            print(f"Message: {content}")
            print("-" * 50)