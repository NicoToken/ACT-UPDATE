# app.py

import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import trading_bot.discord_bot as discord_bot  # Import your modified discord_bot module

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

bot_status = {"running": False}

@app.on_event("startup")
async def startup_event():
    # Start Discord bot when FastAPI starts
    if not discord_bot.client.is_ready():
        await discord_bot.run_bot()

@app.get("/")
async def read_root(request: Request):
    discord_connected = discord_bot.client.is_ready()
    bitget_connected = True  # You can update this based on actual connection status
    bitget_balance = 0  # Update this based on actual balance retrieval logic

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
        asyncio.create_task(discord_bot.run_bot())  # Start Discord bot in background task
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
        await discord_bot.run_bot()
    return RedirectResponse(url="/", status_code=303)

@app.post("/disconnect-discord")
async def disconnect_discord():
    if discord_bot.client.is_ready():
        await discord_bot.stop_discord_bot()
    return RedirectResponse(url="/", status_code=303)

@app.post("/connect-bitget")
async def connect_bitget():
    return RedirectResponse(url="/", status_code=303)

@app.post("/disconnect-bitget")
async def disconnect_bitget():
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
