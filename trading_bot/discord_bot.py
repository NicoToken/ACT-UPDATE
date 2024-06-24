# trading_bot/discord_bot.py

import os
import discord
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import requests
import hmac
import hashlib
import base64

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_API_SECRET = os.getenv('BITGET_API_SECRET')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def sign_request(params, secret):
    params_str = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    digest = hmac.new(secret.encode(), params_str.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()

def get_balance():
    try:
        url = "https://api.bitget.com/api/futures/v1/account/accounts"
        timestamp = str(int((datetime.utcnow() + timedelta(seconds=30)).timestamp() * 1000))
        params = {
            'timestamp': timestamp
        }
        sign = sign_request(params, BITGET_API_SECRET)
        headers = {
            'ACCESS-KEY': BITGET_API_KEY,
            'ACCESS-SIGN': sign,
            'ACCESS-TIMESTAMP': timestamp
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        available_balance = 0
        for item in data['data']:
            if item['symbol'] == 'USDT':
                available_balance = float(item['available'])
                break
        return available_balance
    except Exception as e:
        print(f"Error in get_balance: {e}")
        return 0

def place_order(symbol, side, quantity, price, stop_price):
    try:
        url = "https://api.bitget.com/api/futures/v1/order/place"
        timestamp = str(int((datetime.utcnow() + timedelta(seconds=30)).timestamp() * 1000))
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            'timestamp': timestamp
        }
        sign = sign_request(params, BITGET_API_SECRET)
        headers = {
            'ACCESS-KEY': BITGET_API_KEY,
            'ACCESS-SIGN': sign,
            'ACCESS-TIMESTAMP': timestamp
        }
        response = requests.post(url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if '$' not in message.content:
        return

    try:
        lines = message.content.split('\n')
        ticker_line = lines[0]
        entry_line = lines[3]
        invalidation_line = lines[4]
        targets_line = lines[5]

        symbol = ticker_line.split()[0][1:] + 'USDT'
        entry_price = float(entry_line.split(':')[1].strip())
        invalidation_price = float(invalidation_line.split(':')[1].strip())
        targets = [float(price) for price in targets_line.split(':')[1].split('|')]

        side = "BUY" if entry_price < targets[0] else "SELL"

        available_balance = get_balance()
        trade_amount = available_balance * 0.03
        leverage = 10
        quantity = trade_amount / entry_price * leverage

        order = place_order(symbol, side, quantity, entry_price, invalidation_price)
        if order:
            print(f"Order placed: {order}")
            await message.channel.send(f"Order placed: {order}")  # Optionally send confirmation back to Discord
        else:
            print("Failed to place order.")
            await message.channel.send("Failed to place order.")  # Optionally send failure message back to Discord
    except Exception as e:
        print(f"An error occurred while processing the message: {e}")
        await message.channel.send(f"An error occurred: {e}")  # Optionally send error message back to Discord

async def start_discord_bot():
    try:
        await client.start(DISCORD_TOKEN)
    except discord.LoginFailure as e:
        print(f"Failed to log in to Discord: {e}")
        raise  # Reraise the exception to propagate it up

async def stop_discord_bot():
    await client.close()
