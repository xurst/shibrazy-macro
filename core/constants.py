import os
from dotenv import load_dotenv

load_dotenv()

# Detailed server and channel configurations including webhooks and message filters
SERVER_CONFIGS = {
    1186570213025487912: { # server id
        "name": "name_of_server",
        "channels": {
            "1282542323591481417": { # channel id
                "name": "name_of_channel",
                "webhook_url": os.getenv('EXAMPLE_WEBHOOK'), # what it would look like
                "whitelist": {
                    "keywords": ["keyword 1", "keyword 2", "keyword 3"], # ex: u can put glitch or anything u want in the keywords
                    "match_any": True  # If True, matches if any keyword is found
                },
                "blacklist": {
                    "keywords": ["keyword 1", "keyword 2", "keyword 3"], # ex: u can put glitch or anything u want in the keywords, and it won't join those links.
                    "match_any": True  # If True, blocks if any keyword is found
                }
            },
        }
    },
}

# Time delays for rate limiting and message checking (in seconds)
CHECK_DELAY = 0.05  # Delay between checking messages
RATE_LIMIT_DELAY = 0.1  # Delay when hitting Discord rate limits
WHITELIST_MATCH_RATIO = 75  # Minimum percentage match required for whitelist keywords
BLACKLIST_MATCH_RATIO = 90  # Minimum percentage match required for blacklist keywords

# Link processing configuration
OVERLAPPING = False  # If True, allows joining multiple links without waiting
TIMER_SECONDS = 20  # Cooldown period between joining links

# Debug and output configuration
SEPARATE_TERMINAL = False  # Whether to use a separate terminal window for output
ACTUAL_JOINING = False  # If True, actually joins games; if False, debug mode only

# Message output configuration
PRINT_WHITELISTED_ONLY = False  # If True, only prints messages matching whitelist
PRINT_WHEN_DISABLED = False  # If True, continues printing even when bot is disabled

# Webhook functionality toggle
WEBHOOKING = False  # Controls whether webhook messages are sent

# Hotkey configuration for toggling bot state
TOGGLE_HOTKEY = 'ctrl+y'  # Keyboard shortcut to enable/disable the bot

# Emulator configuration for game joining
USE_EMULATOR = False  # Whether to use emulator for game joining
ADB_PATH = "C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe"  # Path to BlueStacks executable
BLUESTACKS_INSTANCE = "Nougat32"  # Name of BlueStacks instance to use

# MISC
PLAY_SOUND = False # If True, when a keyword is found it will play a sound.
project_root = os.path.dirname(__file__)
SOUND_DIR = os.path.join(project_root, "sounds", "keyword_find")
SOUND_VOLUME = 0.5