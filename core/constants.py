import os
from dotenv import load_dotenv

load_dotenv()

# Detailed server and channel configurations including webhooks and message filters
SERVER_CONFIGS = {
    1186570213077041233: {
        "name": "Sol's RNG",
        "channels": {
            "1282542323590496277": {
                "name": "biomes",
                "webhook_url": "https://discord.com/api/webhooks/1313152326348968018/OF30xUuuUq4pepL7hGrRVsbrJoY9-vfGNT2YsrBuG_Ilnxw6ILsXlYJHpjVcMN2Vwqo4",
                "whitelist": {
                    "keywords": ["glitch", "glitched"],
                    "match_any": True  # If True, matches if any keyword is found
                },
                "blacklist": {
                    "keywords": ["bait", "fake", "scam", "where", "not", "baiters", "unreal", "totally", "astrald", "hunting", "hunt"],
                    "match_any": True  # If True, blocks if any keyword is found
                }
            },
        }
    },
    1284692110242746441: {
        "name": "Radiant Team",
        "channels": {
            "1287614809705021470": {
                "name": "glitch-ping-radiant",
                "webhook_url": "https://discord.com/api/webhooks/1313457406868721735/WwrR0a6w_ckc1BbjAbavi5qxmvxyosMYcsZMnXdxsWaLztqKCXnCg_RolRfeSApmKwOw",
                "whitelist": {
                    "keywords": ["glitch", "glitched", "<@&1287615051888594944>"],
                    "match_any": True
                },
                "blacklist": {
                    "keywords": [],
                    "match_any": True
                }
            },
        }
    }
}

# Time delays for rate limiting and message checking (in seconds)
CHECK_DELAY = 0.05  # Delay between checking messages
RATE_LIMIT_DELAY = 0.1  # Delay when hitting Discord rate limits
WHITELIST_MATCH_RATIO = 75  # Minimum percentage match required for whitelist keywords
BLACKLIST_MATCH_RATIO = 90  # Minimum percentage match required for blacklist keywords

# Link processing configuration
OVERLAPPING = False  # If True, allows joining multiple links without waiting
TIMER_SECONDS = 5  # Cooldown period between joining links

# Debug and output configuration
SEPARATE_TERMINAL = True  # Whether to use a separate terminal window for output
ACTUAL_JOINING = True  # If True, actually joins games; if False, debug mode only

# Message output configuration
PRINT_WHITELISTED_ONLY = False  # If True, only prints messages matching whitelist
PRINT_WHEN_DISABLED = True  # If True, continues printing even when bot is disabled

# Webhook functionality toggle
WEBHOOKING = False  # Controls whether webhook messages are sent

# Hotkey configuration for toggling bot state
TOGGLE_HOTKEY = 'ctrl+y'  # Keyboard shortcut to enable/disable the bot

# Emulator configuration for game joining
USE_EMULATOR = True  # Whether to use emulator for game joining
ADB_PATH = "C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe"  # Path to BlueStacks executable
BLUESTACKS_INSTANCE = "Nougat32"  # Name of BlueStacks instance to use

# MISC
PLAY_SOUND = True # If True, when a keyword is found it will play a sound.
SOUND_DIR = "C:\\Users\\xurst\\Documents\\coding_projects\\discord_bot_projects\\python self bot test\\sounds\\keyword_find"
SOUND_VOLUME = 1