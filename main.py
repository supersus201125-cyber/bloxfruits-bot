import requests
import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

API_TOKEN = '8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w'
CHAT_ID = '-1003378537484'  # ID вашего канала, группы или пользователя

bot = Bot(token=API_TOKEN, parse_mode="Markdown")

def get_stock():
    try:
        r = requests.get("https://bloxfruitstock.com/api/stock", timeout=10)
        r.raise_for_status()
        data = r.json()
        fruits = data.get("stock", [])
        expires = data.get("expiresAt", "")
        text = (
            f"🍏 *Обычный сток фруктов Blox Fruits:*\n" +
            "\n".join([f"• {fruit}" for fruit in fruits])
        )
        if expires:
            text += f"\n\nСледующее обновление: {expires.replace('T', ' ').replace('Z', '')}"
        return text
    except Exception as e:
        return f"❌ Не удалось получить обычный сток: {e}"

def get_mirage():
    try:
        r = requests.get("https://bloxfruitstock.com/api/mirage", timeout=10)
        r.raise_for_status()
        data = r.json()
        mirage = data.get("fruit")  # зависит от структуры, уточните!
        found = data.get("found", False)
        if found and mirage:
            return f"🌟 *Новый Миражный фрукт в стоке*: {mirage}"
        else:
            return None  # не слать ничего если миража нет
    except Exception as e:
        return f"❌ Не удалось получить миражный фрукт: {e}"

async def send_stock():
    stock_text = get_stock()
    await bot.send_message(CHAT_ID, stock_text)

async def send_mirage():
    mirage_text = get_mirage()
    if mirage_text:
        await bot.send_message(CHAT_ID, mirage_text)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_stock, "interval", hours=4)     # Обычный сток каждые 4 часа
    scheduler.add_job(send_mirage, "interval", hours=2)    # Мираж каждый 2 часа
    scheduler.start()
    print("Бот запущен и авто-отправляет сообщения...")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
