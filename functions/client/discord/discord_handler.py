import discum
from core.constants import *
from dotenv import load_dotenv
import os
import time
from discord import Webhook, Embed
import aiohttp
import asyncio
from datetime import datetime
import dateutil.parser

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class DiscordHandler:
    def __init__(self):
        self.bot = discum.Client(token=DISCORD_TOKEN, log=False, build_num=169669)
        self.server_channels = {}

        # Create event loop and session
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.session = self.loop.run_until_complete(self._create_session())

        # Initialize server and channel tracking
        for server_id, config in SERVER_CONFIGS.items():
            self.server_channels[server_id] = list(config['channels'].keys())

    async def _create_session(self):
        return aiohttp.ClientSession()

    def get_latest_message(self, channel_id):
        try:
            messages = self.bot.getMessages(channelID=channel_id, num=1).json()
            if len(messages) > 0:
                return messages[0]
            return None
        except Exception as e:
            time.sleep(RATE_LIMIT_DELAY)
            print(f"Rate limited, waiting... ({str(e)})")
            return None

    def get_channel_config(self, server_id, channel_id):
        server_config = SERVER_CONFIGS.get(server_id)
        if server_config:
            return server_config['channels'].get(channel_id)
        return None

    def send_webhook_message(self, channel_name, message, matched_keywords=None):
        if not WEBHOOKING:
            return

        # Find the webhook URL for the channel
        webhook_url = None
        for server_config in SERVER_CONFIGS.values():
            for channel_config in server_config['channels'].values():
                if channel_config['name'] == channel_name and 'webhook_url' in channel_config:
                    webhook_url = channel_config['webhook_url']
                    break
            if webhook_url:
                break

        if not webhook_url:
            return

        async def send():
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, session=session)

                # Get current timestamp
                timestamp = message.get('timestamp', None)

                # Create a rich embed with custom styling
                embed = Embed(
                    title="🔍 New Message Detected",
                    color=0x2b2d31,  # Discord dark theme color
                    timestamp=dateutil.parser.parse(timestamp) if timestamp else datetime.utcnow()
                )

                # Set author with user avatar if available
                avatar_url = f"https://cdn.discordapp.com/avatars/{message['author']['id']}/{message['author']['avatar']}.png" if \
                message['author'].get('avatar') else None
                embed.set_author(
                    name=message['author']['username'],
                    icon_url=avatar_url
                )

                # Add server and channel context with emojis
                embed.add_field(
                    name="📍 Location",
                    value=f"Channel: {channel_name}",
                    inline=True
                )

                # Add user ID with styling
                embed.add_field(
                    name="👤 User ID",
                    value=f"`{message['author']['id']}`",
                    inline=True
                )

                # Add timestamp field
                embed.add_field(
                    name="⏰ Timestamp",
                    value=f"<t:{int(dateutil.parser.parse(timestamp).timestamp())}:R>" if timestamp else "Just now",
                    inline=True
                )

                # Add message content with formatting
                content = message['content']
                url = None

                # Improved URL and content separation
                if "https://www.roblox.com/share?code=" in content:
                    # Find the URL in the content
                    import re
                    url_match = re.search(r'(https://www\.roblox\.com/share\?code=[^\s]+)', content)
                    if url_match:
                        url = url_match.group(1)
                        # Remove the URL from content and get the remaining text
                        content = content.replace(url, '').strip()

                # Handle content display
                if len(content) > 1024:
                    content = content[:1021] + "..."

                # Always show message content section
                embed.add_field(
                    name="💬 Message Content",
                    value=f"```{content if content else 'No additional content'}```",
                    inline=False
                )

                # Add URL field if present
                if url:
                    embed.add_field(
                        name="🔗 Game Link",
                        value=url,
                        inline=False
                    )

                # Add matched keywords if any, with special formatting
                if matched_keywords:
                    keyword_display = " • ".join(f"`{keyword}`" for keyword in matched_keywords)
                    embed.add_field(
                        name="🎯 Matched Keywords",
                        value=keyword_display,
                        inline=False
                    )

                # Add footer
                embed.set_footer(
                    text="diddy was here",
                    icon_url="https://cdn.discordapp.com/emojis/1039590248859627523.webp?size=96&quality=lossless"
                )

                try:
                    await webhook.send(embed=embed)
                    print(f"\nWebhook sent successfully for channel: {channel_name}")
                except Exception as e:
                    print(f"Error sending webhook: {e}")

        asyncio.run(send())

    async def cleanup(self):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.loop and not self.loop.is_closed():
            self.loop.close()