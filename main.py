import requests
import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

API_TOKEN = '8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w'
CHAT_ID = '-1003378537484'  # ID вашей группы, канала или пользователя

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
LAST_STOCK = None

def fetch_stock():
    try:
        r = requests.get("https://bloxfruitstock.com/api/stock", timeout=10)
        if r.status_code != 200:
            return [], f"❌ Сервер вернул {r.status_code}: {r.text}"
        data = r.json()
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
    if startup or fruits != LAST_STOCK:
        LAST_STOCK = fruits
        await bot.send_message(CHAT_ID, text)

async def periodic_checker():
    scheduler = AsyncIOScheduler(timezone=pytz.UTC)  # Вот тут фикс таймзоны!
    scheduler.add_job(send_stock, "interval", minutes=7)
    scheduler.start()
    while True:
        await asyncio.sleep(3600)

async def main():
    try:
        await send_stock(startup=True)
        await periodic_checker()
    finally:
        await bot.session.close()      # Корректное завершение

if __name__ == "__main__":
    asyncio.run(main())
