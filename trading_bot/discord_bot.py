# trading_bot/discord_bot.py

import os
import discord
from dotenv import load_dotenv
import aiohttp

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def start_discord_bot():
    try:
        await client.start(DISCORD_TOKEN)
    except discord.LoginFailure as e:
        print(f"Failed to log in to Discord: {e}")
        raise  # Reraise the exception to propagate it up

async def stop_discord_bot():
    await client.close()

async def send_message_to_discord(message):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("Channel not found")

async def fetch_bitget_data():
    url = "https://api.bitget.com/api/futures/v1/account/accounts"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
