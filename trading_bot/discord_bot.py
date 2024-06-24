import os
import discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

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
        await client.start(DISCORD_TOKEN)
    except discord.LoginFailure as e:
        print(f"Failed to log in to Discord: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

async def stop_discord_bot():
    await client.close()

async def run_bot():
    try:
        await start_discord_bot()
    finally:
        await client.close()

# In app.py, modify start_bot to use run_bot instead
