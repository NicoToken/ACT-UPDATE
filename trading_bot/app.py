# trading_bot/app.py

import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import discord_bot

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_API_SECRET = os.getenv('BITGET_API_SECRET')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store bot status
bot_status = {"running": False}

async def send_discord_message(message: str):
    try:
        await discord_bot.send_message_to_discord(message)
        return {"status": "Message sent to Discord"}
    except Exception as e:
        return {"status": f"Failed to send message: {str(e)}"}

# Your FastAPI route definitions here
@app.get("/")
async def read_root(request: Request):
    discord_connected = discord_bot.client.is_ready() if discord_bot.client.is_ready() else False
    bitget_connected = True  # Assuming Bitget is always connected in this context
    bitget_balance = 0

    return templates.TemplateResponse("index.html", {
        "request": request,
        "discord_connected": discord_connected,
        "bitget_connected": bitget_connected,
        "bitget_balance": bitget_balance,
        "bot_status": bot_status["running"]
    })

@app.post("/start-bot")
async def start_bot():
    if not bot_status["running"]:
        bot_status["running"] = True
        asyncio.create_task(discord_bot.start_discord_bot())  # Start Discord bot in background task
    return RedirectResponse(url="/", status_code=303)

@app.post("/stop-bot")
async def stop_bot():
    if bot_status["running"]:
        bot_status["running"] = False
        await discord_bot.stop_discord_bot()  # Stop Discord bot
    return RedirectResponse(url="/", status_code=303)

@app.post("/connect-discord")
async def connect_discord():
    if not discord_bot.client.is_ready():
        await discord_bot.start_discord_bot()
    return RedirectResponse(url="/", status_code=303)

@app.post("/disconnect-discord")
async def disconnect_discord():
    if discord_bot.client.is_ready():
        await discord_bot.stop_discord_bot()
    return RedirectResponse(url="/", status_code=303)

@app.post("/connect-bitget")
async def connect_bitget():
    # Logic to connect Bitget API if needed
    return RedirectResponse(url="/", status_code=303)

@app.post("/disconnect-bitget")
async def disconnect_bitget():
    # Logic to disconnect Bitget API if needed
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
