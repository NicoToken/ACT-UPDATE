# trading_bot/discord_bot.py

import os
import discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in environment variables.")
if not CHANNEL_ID:
    raise ValueError("DISCORD_CHANNEL_ID is not set in environment variables.")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def send_message_to_discord(message):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("Channel not found")

async def start_discord_bot():
    try:
        print(f"Using DISCORD_TOKEN: '{DISCORD_TOKEN.strip()}'")  # Debug print, remove in production
        await client.start(DISCORD_TOKEN.strip())
    except discord.LoginFailure as e:
        print(f"Failed to log in to Discord: {e}")
        raise  # Reraise the exception to propagate it up

async def stop_discord_bot():
    await client.close()
