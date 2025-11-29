import requests
import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

API_TOKEN = '8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w'
CHAT_ID = '-1003378537484'  # ID вашего канала, группы или пользователя

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode="Markdown")
)
LAST_STOCK = None  # Глобальная переменная для хранения предыд. стока

def fetch_stock():
    try:
        data = requests.get("https://bloxfruitstock.com/api/stock", timeout=10).json()
        fruits = data.get("stock", [])
        expires = data.get("expiresAt", "")
        text = (
            f"🍏 *Сток фруктов Blox Fruits:*\n"
            + "\n".join([f"• {fruit}" for fruit in fruits])
        )
        if expires:
            text += f"\n\nСледующее обновление: {expires.replace('T', ' ').replace('Z', '')}"
        return fruits, text
    except Exception as e:
        return [], f"❌ Не удалось получить сток фруктов: {e}"

async def send_stock(startup=False):
    global LAST_STOCK
    fruits, text = fetch_stock()
    # При запуске всегда отправляет сообщение
    if startup or fruits != LAST_STOCK:
        LAST_STOCK = fruits
        await bot.send_message(CHAT_ID, text)

async def periodic_checker():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_stock, "interval", minutes=7)
    scheduler.start()
    while True:
        await asyncio.sleep(3600)

async def main():
    await send_stock(startup=True)  # При запуске отправляет всегда!
    await periodic_checker()

if __name__ == "__main__":
    asyncio.run(main())
