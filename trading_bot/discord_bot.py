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
    await client.start(DISCORD_TOKEN)

async def stop_discord_bot():
    await client.close()
